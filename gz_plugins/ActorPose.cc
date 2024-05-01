#include <string>

#include <gz/plugin/Register.hh>
#include <gz/transport/Node.hh>
#include <gz/common/Profiler.hh>

#include <gz/sim/components/Actor.hh>
#include <gz/sim/components/Name.hh>
#include <gz/sim/components/Pose.hh>

#include <gz/sim/EntityComponentManager.hh>
#include <gz/sim/Util.hh>

#include "ActorPose.hh"

using namespace ignition;
using namespace gazebo;
using namespace systems;

class ignition::gazebo::systems::ActorPosePrivate
{
  /// \brief Entity for the actor.
  public: Entity actorEntity{kNullEntity};
  
  public: msgs::Pose poseMsg;

  public: transport::Node node;

  public: transport::Node::Publisher posePub;
  
  public: double updateFrequency = -1;

  public: std::chrono::steady_clock::duration updatePeriod{0};

  /// \brief Time of the last update.
  public: std::chrono::steady_clock::duration lastUpdate{0};

};

//////////////////////////////////////////////////
ActorPose::ActorPose() :
  System(), dataPtr(std::make_unique<ActorPosePrivate>())
{
}

//////////////////////////////////////////////////
ActorPose::~ActorPose() = default;

//////////////////////////////////////////////////
void ActorPose::Configure(const Entity &_entity,
    const std::shared_ptr<const sdf::Element> &_sdf,
    EntityComponentManager &_ecm,
    EventManager &/*_eventMgr*/)
{
  this->dataPtr->actorEntity = _entity;

  std::string poseTopic = scopedName(_entity, _ecm) + "/pose";

  poseTopic = transport::TopicUtils::AsValidTopic(poseTopic);

  this->dataPtr->posePub = this->dataPtr->node.Advertise<msgs::Pose>(poseTopic);

  if (this->dataPtr->updateFrequency > 0)
  {
    std::chrono::duration<double> period{1 / this->dataPtr->updateFrequency};
    this->dataPtr->updatePeriod =
        std::chrono::duration_cast<std::chrono::steady_clock::duration>(period);
  }

}

//////////////////////////////////////////////////

void ActorPose::PostUpdate(const UpdateInfo &_info,
    const EntityComponentManager &_ecm)
{
    IGN_PROFILE("ActorPose::PostUpdate");

    if (_info.dt < std::chrono::steady_clock::duration::zero())
    {
        ignwarn << "Detected jump back in time ["
            << std::chrono::duration_cast<std::chrono::seconds>(_info.dt).count()
            << "s]. System may not work properly." << std::endl;
    }

    if (_info.paused)
    return;

    bool publish = true;

    auto diff = _info.simTime - this->dataPtr->lastUpdate;

    if ((diff > std::chrono::steady_clock::duration::zero()) &&
      (diff < this->dataPtr->updatePeriod))
    {
        publish = false;
    }
    if (!publish)
        return;
    
    auto actorpose = _ecm.Component<components::WorldPose>(this->dataPtr->actorEntity);

    msgs::Pose *msg = nullptr;
    this->dataPtr->poseMsg.Clear();
    msg = &this->dataPtr->poseMsg;
    
    auto timeStamp = convert<msgs::Time>(_info.simTime);
    auto header = msg->mutable_header();
    header->mutable_stamp()->CopyFrom(timeStamp);
    const math::Pose3d &transform = actorpose->Data();  
    auto frame = header->add_data();
    msg->set_name(_ecm.Component<components::Name>(this->dataPtr->actorEntity)->Data());
    msgs::Set(msg, transform);


    this->dataPtr->posePub.Publish(this->dataPtr->poseMsg);

    // this->dataPtr->PublishPoses(this->dataPtr->poses, convert<msgs::Time>(_info.simTime), this->dataPtr->posePub);

    this->dataPtr->lastUpdate = _info.simTime;
}

IGNITION_ADD_PLUGIN(ActorPose, System,
  ActorPose::ISystemConfigure,
  ActorPose::ISystemPostUpdate
)

IGNITION_ADD_PLUGIN_ALIAS(ActorPose, "ignition::gazebo::systems::ActorPose")

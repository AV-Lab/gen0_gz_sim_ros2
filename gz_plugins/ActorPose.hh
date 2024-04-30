#ifndef IGNITION_GAZEBO_SYSTEMS_ACTORPOSE_HH_
#define IGNITION_GAZEBO_SYSTEMS_ACTORPOSE_HH_

#include <memory>
#include <gz/sim/config.hh>
#include <gz/sim/System.hh>

namespace ignition
{
namespace gazebo
{
// Inline bracket to help doxygen filtering.
inline namespace IGNITION_GAZEBO_VERSION_NAMESPACE {
namespace systems
{
  // Forward declarations.
  class ActorPosePrivate;

  class ActorPose:
    public System,
    public ISystemConfigure,
    public ISystemPostUpdate
  {
    /// \brief Constructor
    public: explicit ActorPose();

    /// \brief Destructor
    public: ~ActorPose() override;

    // Documentation inherited
    public: void Configure(const Entity &_entity,
                           const std::shared_ptr<const sdf::Element> &_sdf,
                           EntityComponentManager &_ecm,
                           EventManager &_eventMgr) final;
    
    public: void PostUpdate(
            const UpdateInfo &_info,
            const EntityComponentManager &_ecm) final;

    /// \brief Private data pointer.
    private: std::unique_ptr<ActorPosePrivate> dataPtr;
  };
  }
}
}
}
#endif
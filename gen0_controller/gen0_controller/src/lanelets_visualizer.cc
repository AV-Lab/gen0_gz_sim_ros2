  auto sphereStr = R"(
    <?xml version="1.0" ?>
    <sdf version='1.7'>
      <model name='sphere'>
        <link name='link'>
          <pose>0 0 0.5 0 0 0</pose>
          <visual name='visual'>
            <geometry><sphere><radius>1</radius></sphere></geometry>
          </visual>
          <collision name='collision'>
            <geometry><sphere><radius>1</radius></sphere></geometry>
          </collision>
        </link>
      </model>
    </sdf>)";

bool result;
ignition::msgs::EntityFactory req;
ignition::msgs::Boolean res;
req.set_sdf(modelStr);
bool executed = node.Request("/world/empty/create",
          req, timeout, res, result);
if (executed)
{
  if (result)
    std::cout << "Entity was created : [" << res.data() << "]" << std::endl;
  else
  {
    std::cout << "Service call failed" << std::endl;
    return;
  }
}
else
  std::cerr << "Service call timed out" << std::endl;

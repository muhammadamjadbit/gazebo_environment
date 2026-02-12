cmake_minimum_required(VERSION 3.8)
project(cpr_inspection_gazebo)

find_package(ament_cmake REQUIRED)

install(DIRECTORY images launch meshes models rviz scripts urdf worlds
  DESTINATION share/${PROJECT_NAME}
  PATTERN "*~" EXCLUDE)

install(FILES model.config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()

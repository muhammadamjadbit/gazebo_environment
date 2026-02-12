cmake_minimum_required(VERSION 3.8)
project(cpr_office_gazebo)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch meshes rviz urdf worlds
  DESTINATION share/${PROJECT_NAME}
)

install(FILES model.config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()

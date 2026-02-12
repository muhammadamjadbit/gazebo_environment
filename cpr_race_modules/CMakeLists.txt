cmake_minimum_required(VERSION 3.8)
project(gazebo_race_modules)

find_package(ament_cmake REQUIRED)

install(DIRECTORY docs launch meshes urdf worlds
  DESTINATION share/${PROJECT_NAME}
)

install(FILES model.config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()

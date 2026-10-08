cmake_minimum_required(VERSION 3.8)
project(imu_gps_localization)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

set(CMAKE_CXX_STANDARD 14)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(Eigen3 REQUIRED)

include_directories(
  include
  ${EIGEN3_INCLUDE_DIR}
  third_party/GeographicLib/include
)

add_subdirectory(third_party/GeographicLib)

add_library(imu_gps_localizer_lib
  src/base_type.cpp
  src/utils.cpp
  src/initializer.cpp
  src/imu_processor.cpp
  src/gps_processor.cpp
  src/imu_gps_localizer.cpp
)

ament_target_dependencies(imu_gps_localizer_lib
  Eigen3
)

target_link_libraries(imu_gps_localizer_lib
  Geographic
)

add_executable(imu_gps_localization_node
  src/imu_gps_localization_node.cpp
  src/localization_wrapper.cpp
)

ament_target_dependencies(imu_gps_localization_node
  rclcpp
  sensor_msgs
  nav_msgs
  geometry_msgs
  tf2
  tf2_ros
)

target_link_libraries(imu_gps_localization_node
  imu_gps_localizer_lib
)

install(TARGETS
  imu_gps_localization_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  launch
  rviz
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY include/
  DESTINATION include/
)

ament_export_include_directories(include)
ament_export_libraries(imu_gps_localizer_lib)

ament_package()

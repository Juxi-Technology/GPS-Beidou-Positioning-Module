cmake_minimum_required(VERSION 3.8)
project(nmea_navsat_driver)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(nmea_msgs REQUIRED)

add_executable(gps_path src/gps_path.cpp)
ament_target_dependencies(gps_path
  rclcpp
  sensor_msgs
  geometry_msgs
  nav_msgs
)

install(TARGETS
  gps_path
  DESTINATION lib/${PROJECT_NAME}
)

ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  scripts/nmea_serial_driver.py
  scripts/nmea_socket_driver.py
  scripts/nmea_topic_driver.py
  scripts/read_lat_long.py
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  launch
  rviz
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()

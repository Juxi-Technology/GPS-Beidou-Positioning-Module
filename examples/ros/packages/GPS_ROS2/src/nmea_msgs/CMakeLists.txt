cmake_minimum_required(VERSION 3.8)
project(nmea_msgs)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)

set(msg_files
  "msg/Gpgga.msg"
  "msg/Gpgsa.msg"
  "msg/Gpgst.msg"
  "msg/Gpgsv.msg"
  "msg/GpgsvSatellite.msg"
  "msg/Gprmc.msg"
  "msg/Sentence.msg"
)

rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  DEPENDENCIES std_msgs
)

ament_export_dependencies(rosidl_default_runtime)

ament_package()

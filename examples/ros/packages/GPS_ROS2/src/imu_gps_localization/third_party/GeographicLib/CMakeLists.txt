project(GeographicLib)

set(PROJECT_VERSION_MAJOR 1)
set(PROJECT_VERSION_MINOR 49)
set(PROJECT_VERSION_PATCH 0)
set(PROJECT_VERSION "${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}")
if(PROJECT_VERSION_PATCH GREATER 0)
  set(PROJECT_VERSION "${PROJECT_VERSION}.${PROJECT_VERSION_PATCH}")
endif()

set(GEOGRAPHICLIB_PRECISION 2 CACHE STRING
  "Precision: 1 = float, 2 = double, 3 = extended, 4 = quadruple, 5 = variable")
set_property(CACHE GEOGRAPHICLIB_PRECISION PROPERTY STRINGS 1 2 3 4 5)

include_directories(./include/)

add_library(Geographic
  src/LocalCartesian.cpp
  src/Geocentric.cpp
  src/Math.cpp
)

target_include_directories(Geographic PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

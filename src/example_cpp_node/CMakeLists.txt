cmake_minimum_required(VERSION 3.8)
project(example_cpp_node)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(example_msgs REQUIRED)

# Publisher executable
add_executable(publisher src/publisher_node.cpp)
ament_target_dependencies(publisher rclcpp example_msgs)

# Subscriber executable
add_executable(subscriber src/subscriber_node.cpp)
ament_target_dependencies(subscriber rclcpp example_msgs)

# Install executables
install(TARGETS
  publisher
  subscriber
  DESTINATION lib/${PROJECT_NAME})

# Testing
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  find_package(ament_cmake_gtest REQUIRED)

  # Linting
  ament_lint_auto_find_test_dependencies()

  # Add gtest
  ament_add_gtest(${PROJECT_NAME}_test test/test_example_nodes.cpp)
  target_include_directories(${PROJECT_NAME}_test PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)
  ament_target_dependencies(${PROJECT_NAME}_test rclcpp example_msgs)
endif()

ament_package()

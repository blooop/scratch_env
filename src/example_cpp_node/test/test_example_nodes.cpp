/**
 * @file test_example_nodes.cpp
 * @brief Tests for example C++ nodes
 */

#include <gtest/gtest.h>

#include <memory>

#include "example_msgs/msg/example_message.hpp"
#include "rclcpp/rclcpp.hpp"

class TestExampleNodes : public ::testing::Test {
 protected:
  static void SetUpTestCase() { rclcpp::init(0, nullptr); }

  static void TearDownTestCase() { rclcpp::shutdown(); }
};

TEST_F(TestExampleNodes, TestMessageCreation) {
  auto message = example_msgs::msg::ExampleMessage();
  message.name = "test_message";
  message.value = 42;
  message.timestamp = 123.456;
  message.is_active = true;

  EXPECT_EQ(message.name, "test_message");
  EXPECT_EQ(message.value, 42);
  EXPECT_DOUBLE_EQ(message.timestamp, 123.456);
  EXPECT_TRUE(message.is_active);
}

TEST_F(TestExampleNodes, TestNodeCreation) {
  auto node = rclcpp::Node::make_shared("test_node");
  EXPECT_EQ(node->get_name(), std::string("test_node"));
}

int main(int argc, char** argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}

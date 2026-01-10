/**
 * @file subscriber_node.cpp
 * @brief Example ROS2 subscriber node using custom messages in C++
 */

#include <memory>

#include "example_msgs/msg/example_message.hpp"
#include "rclcpp/rclcpp.hpp"

class ExampleSubscriber : public rclcpp::Node {
 public:
  ExampleSubscriber() : Node("example_subscriber_cpp") {
    subscription_ = this->create_subscription<example_msgs::msg::ExampleMessage>(
        "example_topic_cpp", 10,
        std::bind(&ExampleSubscriber::topic_callback, this, std::placeholders::_1));
    RCLCPP_INFO(this->get_logger(), "Example Subscriber C++ Node started");
  }

 private:
  void topic_callback(const example_msgs::msg::ExampleMessage::SharedPtr msg) const {
    RCLCPP_INFO(this->get_logger(),
                "Received: name='%s', value=%d, timestamp=%f, is_active=%s",
                msg->name.c_str(), msg->value, msg->timestamp,
                msg->is_active ? "true" : "false");
  }

  rclcpp::Subscription<example_msgs::msg::ExampleMessage>::SharedPtr subscription_;
};

int main(int argc, char* argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ExampleSubscriber>());
  rclcpp::shutdown();
  return 0;
}

/**
 * @file publisher_node.cpp
 * @brief Example ROS2 publisher node using custom messages in C++
 */

#include <chrono>
#include <memory>

#include "example_msgs/msg/example_message.hpp"
#include "rclcpp/rclcpp.hpp"

using namespace std::chrono_literals;

class ExamplePublisher : public rclcpp::Node {
 public:
  ExamplePublisher() : Node("example_publisher_cpp"), count_(0) {
    publisher_ = this->create_publisher<example_msgs::msg::ExampleMessage>(
        "example_topic_cpp", 10);
    timer_ = this->create_wall_timer(
        1000ms, std::bind(&ExamplePublisher::timer_callback, this));
    RCLCPP_INFO(this->get_logger(), "Example Publisher C++ Node started");
  }

 private:
  void timer_callback() {
    auto message = example_msgs::msg::ExampleMessage();
    message.name = "cpp_message_" + std::to_string(count_);
    message.value = count_;
    message.timestamp = this->now().seconds();
    message.is_active = true;

    RCLCPP_INFO(this->get_logger(), "Publishing: name='%s', value=%d, timestamp=%f",
                message.name.c_str(), message.value, message.timestamp);
    publisher_->publish(message);
    count_++;
  }

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<example_msgs::msg::ExampleMessage>::SharedPtr publisher_;
  int count_;
};

int main(int argc, char* argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ExamplePublisher>());
  rclcpp::shutdown();
  return 0;
}

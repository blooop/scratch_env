#!/usr/bin/env python3
"""Example ROS2 publisher node using custom messages."""

import time

import rclpy
from example_msgs.msg import ExampleMessage
from rclpy.node import Node


class ExamplePublisher(Node):
    """Publishes example messages at a fixed rate."""

    def __init__(self):
        super().__init__("example_publisher")
        self.publisher_ = self.create_publisher(ExampleMessage, "example_topic", 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0
        self.get_logger().info("Example Publisher Node started")

    def timer_callback(self):
        """Publish a message on each timer tick."""
        msg = ExampleMessage()
        msg.name = f"message_{self.count}"
        msg.value = self.count
        msg.timestamp = time.time()
        msg.is_active = True
        self.publisher_.publish(msg)
        self.get_logger().info(
            f'Publishing: name="{msg.name}", value={msg.value}, timestamp={msg.timestamp}'
        )
        self.count += 1


def main(args=None):
    """Main entry point for the publisher node."""
    rclpy.init(args=args)
    node = ExamplePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

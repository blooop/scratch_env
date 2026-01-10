#!/usr/bin/env python3
"""Example ROS2 subscriber node using custom messages."""

import rclpy
from example_msgs.msg import ExampleMessage
from rclpy.node import Node


class ExampleSubscriber(Node):
    """Subscribes to example messages and logs them."""

    def __init__(self):
        super().__init__("example_subscriber")
        self.subscription = self.create_subscription(
            ExampleMessage, "example_topic", self.listener_callback, 10
        )
        self.get_logger().info("Example Subscriber Node started")

    def listener_callback(self, msg):
        """Handle received messages."""
        self.get_logger().info(
            f'Received: name="{msg.name}", value={msg.value}, '
            f"timestamp={msg.timestamp}, is_active={msg.is_active}"
        )


def main(args=None):
    """Main entry point for the subscriber node."""
    rclpy.init(args=args)
    node = ExampleSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

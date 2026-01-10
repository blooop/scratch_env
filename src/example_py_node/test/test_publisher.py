#!/usr/bin/env python3
"""Tests for the example publisher node."""

import time
import unittest

import rclpy
from example_msgs.msg import ExampleMessage
from example_py_node.publisher_node import ExamplePublisher


class TestExamplePublisher(unittest.TestCase):
    """Test cases for ExamplePublisher."""

    @classmethod
    def setUpClass(cls):
        """Initialize ROS2 for testing."""
        rclpy.init()

    @classmethod
    def tearDownClass(cls):
        """Shutdown ROS2 after testing."""
        rclpy.shutdown()

    def setUp(self):
        """Set up each test."""
        self.node = ExamplePublisher()

    def tearDown(self):
        """Clean up after each test."""
        self.node.destroy_node()

    def test_node_creation(self):
        """Test that the node is created properly."""
        self.assertEqual(self.node.get_name(), "example_publisher")

    def test_publisher_exists(self):
        """Test that the publisher is created."""
        self.assertIsNotNone(self.node.publisher_)

    def test_message_publishing(self):
        """Test that messages can be created and have correct initial values."""
        msg = ExampleMessage()
        msg.name = "test_message"
        msg.value = 42
        msg.timestamp = time.time()
        msg.is_active = True

        self.assertEqual(msg.name, "test_message")
        self.assertEqual(msg.value, 42)
        self.assertTrue(msg.is_active)
        self.assertGreater(msg.timestamp, 0)


if __name__ == "__main__":
    unittest.main()

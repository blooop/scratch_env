#!/usr/bin/env python3
"""Tests for the example subscriber node."""

import unittest

import rclpy
from example_py_node.subscriber_node import ExampleSubscriber


class TestExampleSubscriber(unittest.TestCase):
    """Test cases for ExampleSubscriber."""

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
        self.node = ExampleSubscriber()

    def tearDown(self):
        """Clean up after each test."""
        self.node.destroy_node()

    def test_node_creation(self):
        """Test that the node is created properly."""
        self.assertEqual(self.node.get_name(), "example_subscriber")

    def test_subscription_exists(self):
        """Test that the subscription is created."""
        self.assertIsNotNone(self.node.subscription)


if __name__ == "__main__":
    unittest.main()

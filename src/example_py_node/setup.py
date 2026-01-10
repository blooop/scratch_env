from setuptools import find_packages, setup

package_name = "example_py_node"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Austin Gregg-Smith",
    maintainer_email="blooop@gmail.com",
    description="Example Python ROS2 nodes using custom messages",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "publisher = example_py_node.publisher_node:main",
            "subscriber = example_py_node.subscriber_node:main",
        ],
    },
)

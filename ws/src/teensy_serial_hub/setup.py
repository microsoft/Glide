from setuptools import setup

package_name = 'teensy_serial_hub'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='joncamp@microsoft.com',
    description='Communication interface for serial communications between teensy and host.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'teensy_serial_hub_node = teensy_serial_hub.teensy_serial_hub:main'
        ],
    },
)

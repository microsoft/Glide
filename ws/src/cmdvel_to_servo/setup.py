from setuptools import setup

package_name = 'cmdvel_to_servo'

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
    description='Converts cmdvel messages into appropriate servo commands',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'cmdvel_to_servo_node = cmdvel_to_servo.cmdvel_to_servo:main'
        ],
    },
)

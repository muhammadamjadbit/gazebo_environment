from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    robot_description = Command([
        'xacro ',
        PathJoinSubstitution([
            FindPackageShare('cpr_empty_gazebo'),
            'urdf',
            'empty_geometry.urdf.xacro'
        ])
    ])
    
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description
        }]
    )
    
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz',
        arguments=['-d', PathJoinSubstitution([
            FindPackageShare('cpr_empty_gazebo'),
            'rviz',
            'world.rviz'
        ])]
    )
    
    return LaunchDescription([
        robot_state_publisher,
        rviz
    ])

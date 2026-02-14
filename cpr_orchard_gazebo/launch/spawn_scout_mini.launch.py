import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command, FindExecutable
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')
    yaw = LaunchConfiguration('yaw')
    use_sim_time = LaunchConfiguration('use_sim_time')
    odometry_source = LaunchConfiguration('odometry_source')
    lidar_type = LaunchConfiguration('lidar_type')
    
    declare_x = DeclareLaunchArgument('x', default_value='0.0')
    declare_y = DeclareLaunchArgument('y', default_value='0.0')
    declare_z = DeclareLaunchArgument('z', default_value='0.0')
    declare_yaw = DeclareLaunchArgument('yaw', default_value='0.0')
    declare_use_sim_time = DeclareLaunchArgument('use_sim_time', default_value='true')
    declare_odometry_source = DeclareLaunchArgument('odometry_source', default_value='ground_truth')
    declare_lidar_type = DeclareLaunchArgument('lidar_type', default_value='3d')
    
    # Scout Mini robot description
    scout_description_file = os.path.join(
        get_package_share_directory("agilex_scout"),
        "urdf",
        "robot.urdf.xacro"
    )
    
    robot_description = ParameterValue(
        Command([
            FindExecutable(name="xacro"),
            " ",
            scout_description_file,
            " odometry_source:=", odometry_source,
            " load_gazebo:=true",
            " simulation:=true",
            " lidar_type:=", lidar_type
        ]),
        value_type=str
    )
    
    # Robot state publisher for Scout Mini
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': use_sim_time
        }],
        remappings=[
            ("/joint_states", "/scout/joint_states"),
            ("/robot_description", "/scout/robot_description"),
        ]
    )
    
    # Spawn Scout Mini in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'scout_mini',
            '-topic', '/scout/robot_description',
            '-x', x,
            '-y', y,
            '-z', z,
            '-Y', yaw,
        ],
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )
    
    return LaunchDescription([
        declare_x,
        declare_y,
        declare_z,
        declare_yaw,
        declare_use_sim_time,
        declare_odometry_source,
        declare_lidar_type,
        robot_state_publisher,
        spawn_entity
    ])

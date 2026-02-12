from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command, EnvironmentVariable
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare arguments
    platform = LaunchConfiguration('platform')
    robot_x = LaunchConfiguration('robot_x')
    robot_y = LaunchConfiguration('robot_y')
    robot_z = LaunchConfiguration('robot_z')
    robot_yaw = LaunchConfiguration('robot_yaw')
    world_x = LaunchConfiguration('world_x')
    world_y = LaunchConfiguration('world_y')
    world_z = LaunchConfiguration('world_z')
    world_yaw = LaunchConfiguration('world_yaw')
    use_sim_time = LaunchConfiguration('use_sim_time')
    gui = LaunchConfiguration('gui')
    headless = LaunchConfiguration('headless')
    world_name = LaunchConfiguration('world_name')
    
    declare_platform = DeclareLaunchArgument(
        'platform',
        default_value=EnvironmentVariable('CPR_GAZEBO_PLATFORM', default_value='scout_mini'),
        description='Robot platform to spawn'
    )
    
    declare_robot_x = DeclareLaunchArgument('robot_x', default_value='0.0')
    declare_robot_y = DeclareLaunchArgument('robot_y', default_value='0.0')
    declare_robot_z = DeclareLaunchArgument('robot_z', default_value='2.0')
    declare_robot_yaw = DeclareLaunchArgument('robot_yaw', default_value='0.0')
    
    declare_world_x = DeclareLaunchArgument('world_x', default_value='0.0')
    declare_world_y = DeclareLaunchArgument('world_y', default_value='0.0')
    declare_world_z = DeclareLaunchArgument('world_z', default_value='0.0')
    declare_world_yaw = DeclareLaunchArgument('world_yaw', default_value='0.0')
    
    declare_use_sim_time = DeclareLaunchArgument('use_sim_time', default_value='true')
    declare_gui = DeclareLaunchArgument('gui', default_value='true')
    declare_headless = DeclareLaunchArgument('headless', default_value='false')
    
    declare_world_name = DeclareLaunchArgument(
        'world_name',
        default_value=PathJoinSubstitution([
            FindPackageShare('cpr_empty_gazebo'),
            'worlds',
            'actually_empty_world.world'
        ])
    )
    
    # Set empty geometry parameter
    empty_geom_param = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='empty_geom_publisher',
        parameters=[{
            'robot_description': Command([
                'xacro ',
                PathJoinSubstitution([
                    FindPackageShare('cpr_empty_gazebo'),
                    'urdf',
                    'empty_geometry.urdf.xacro'
                ])
            ]),
            'use_sim_time': use_sim_time
        }],
        remappings=[('robot_description', 'empty_geom')]
    )
    
    # Launch Gazebo
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            ])
        ]),
        launch_arguments={
            'world': world_name,
            'gui': gui,
            'verbose': 'false'
        }.items()
    )
    
    # Spawn empty world geometry
    spawn_empty = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='empty_world_spawner',
        arguments=[
            '-entity', 'empty_geometry',
            '-topic', 'empty_geom',
            '-x', world_x,
            '-y', world_y,
            '-z', world_z,
            '-Y', world_yaw
        ],
        parameters=[{'use_sim_time': use_sim_time}]
    )
    
    # Include robot spawn launch file
    robot_spawn_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('cpr_empty_gazebo'),
                'launch',
                ['spawn_', platform, '.launch.py']
            ])
        ),
        launch_arguments={
            'x': robot_x,
            'y': robot_y,
            'z': robot_z,
            'yaw': robot_yaw
        }.items()
    )
    
    return LaunchDescription([
        declare_platform,
        declare_robot_x,
        declare_robot_y,
        declare_robot_z,
        declare_robot_yaw,
        declare_world_x,
        declare_world_y,
        declare_world_z,
        declare_world_yaw,
        declare_use_sim_time,
        declare_gui,
        declare_headless,
        declare_world_name,
        empty_geom_param,
        gazebo_launch,
        spawn_empty,
        robot_spawn_launch
    ])

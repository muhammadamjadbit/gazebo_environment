from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare arguments
    world_x = LaunchConfiguration('world_x')
    world_y = LaunchConfiguration('world_y')
    world_z = LaunchConfiguration('world_z')
    world_yaw = LaunchConfiguration('world_yaw')
    use_sim_time = LaunchConfiguration('use_sim_time')
    gui = LaunchConfiguration('gui')
    headless = LaunchConfiguration('headless')
    world_name = LaunchConfiguration('world_name')
    
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
            FindPackageShare('cpr_inspection_gazebo'),
            'worlds',
            'inspection_world.world'
        ])
    )
    
    # Set inspection geometry parameter
    inspection_geom_param = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='inspection_geom_publisher',
        parameters=[{
            'robot_description': Command([
                'xacro ',
                PathJoinSubstitution([
                    FindPackageShare('cpr_inspection_gazebo'),
                    'urdf',
                    'inspection_geometry.urdf.xacro'
                ])
            ]),
            'use_sim_time': use_sim_time
        }],
        remappings=[('robot_description', 'inspection_geom')]
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
    
    # Spawn inspection world geometry
    spawn_inspection = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='inspection_world_spawner',
        arguments=[
            '-entity', 'inspection_geometry',
            '-topic', 'inspection_geom',
            '-x', world_x,
            '-y', world_y,
            '-z', world_z,
            '-Y', world_yaw
        ],
        parameters=[{'use_sim_time': use_sim_time}]
    )
    
    return LaunchDescription([
        declare_world_x,
        declare_world_y,
        declare_world_z,
        declare_world_yaw,
        declare_use_sim_time,
        declare_gui,
        declare_headless,
        declare_world_name,
        inspection_geom_param,
        gazebo_launch,
        spawn_inspection
    ])

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    track_type = LaunchConfiguration('track_type')
    barrier_type = LaunchConfiguration('barrier_type')
    complexity = LaunchConfiguration('complexity')
    size = LaunchConfiguration('size')
    
    declare_track_type = DeclareLaunchArgument(
        'track_type',
        default_value='road',
        description='Type of track'
    )
    
    declare_barrier_type = DeclareLaunchArgument(
        'barrier_type',
        default_value='racing',
        description='Type of barrier'
    )
    
    declare_complexity = DeclareLaunchArgument(
        'complexity',
        default_value='simple',
        description='Complexity level'
    )
    
    declare_size = DeclareLaunchArgument(
        'size',
        default_value='small',
        description='Size of objects'
    )
    
    spawn_world_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('cpr_race_modules'),
                'launch',
                'spawn_world.launch.py'
            ])
        ])
    )
    
    object_descriptions_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('cpr_race_modules'),
                'launch',
                'object_descriptions.launch.py'
            ])
        ]),
        launch_arguments={
            'track_type': track_type,
            'barrier_type': barrier_type,
            'complexity': complexity,
            'size': size
        }.items()
    )
    
    # Define all spawn nodes for straight sections
    straight_nodes = []
    straight_configs = [
        ('straight1', 0, 0, 0, 0),
        ('straight2', 1, 0, 0, 0),
        ('straight3', 2, 1, 0, 1.5707),
        ('straight4', 2, 2, 0, 1.5707),
        ('straight5', 0, 2, 0, 3.14159),
        ('straight6', -1, 2, 0, 3.14159),
        ('straight7', -2, 1, 0, 1.5707),
        ('straight8', -1, 0, 0, 0)
    ]
    
    for name, x, y, z, yaw in straight_configs:
        straight_nodes.append(
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                name=f'{name}_spawner',
                arguments=[
                    '-entity', name,
                    '-topic', 'robot_description',
                    '-x', str(x),
                    '-y', str(y),
                    '-z', str(z),
                    '-Y', str(yaw)
                ],
                parameters=[{'use_sim_time': True}],
                remappings=[('robot_description', 'straight_description')]
            )
        )
    
    # Define all spawn nodes for corner sections
    corner_nodes = []
    corner_configs = [
        ('corner1', 2, 0, 0, 3.14159),
        ('corner2', 2, 3, 0, -1.5707),
        ('corner3', 1, 3, 0, 0),
        ('corner4', 1, 2, 0, 3.14159),
        ('corner5', -2, 2, 0, 0),
        ('corner6', -2, 0, 0, 1.5707)
    ]
    
    for name, x, y, z, yaw in corner_configs:
        corner_nodes.append(
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                name=f'{name}_spawner',
                arguments=[
                    '-entity', name,
                    '-topic', 'robot_description',
                    '-x', str(x),
                    '-y', str(y),
                    '-z', str(z),
                    '-Y', str(yaw)
                ],
                parameters=[{'use_sim_time': True}],
                remappings=[('robot_description', 'corner_description')]
            )
        )
    
    # Define all spawn nodes for edge straight sections
    edge_straight_nodes = []
    edge_straight_configs = [
        ('edge_straight1', 0, 0, 0, 0),
        ('edge_straight2', 1, 0, 0, 0),
        ('edge_straight3', 2, 1, 0, 1.5707),
        ('edge_straight4', 2, 2, 0, 1.5707),
        ('edge_straight5', 0, 2, 0, 3.14159),
        ('edge_straight6', -1, 2, 0, 3.14159),
        ('edge_straight7', -2, 1, 0, 1.5707),
        ('edge_straight8', -1, 0, 0, 0)
    ]
    
    for name, x, y, z, yaw in edge_straight_configs:
        edge_straight_nodes.append(
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                name=f'{name}_spawner',
                arguments=[
                    '-entity', name,
                    '-topic', 'robot_description',
                    '-x', str(x),
                    '-y', str(y),
                    '-z', str(z),
                    '-Y', str(yaw)
                ],
                parameters=[{'use_sim_time': True}],
                remappings=[('robot_description', 'edge_straight_description')]
            )
        )
    
    # Define all spawn nodes for edge corner sections
    edge_corner_nodes = []
    edge_corner_configs = [
        ('edge_corner1', 2, 0, 0, 3.14159),
        ('edge_corner2', 2, 3, 0, -1.5707),
        ('edge_corner3', 1, 3, 0, 0),
        ('edge_corner4', 1, 2, 0, 3.14159),
        ('edge_corner5', -2, 2, 0, 0),
        ('edge_corner6', -2, 0, 0, 1.5707)
    ]
    
    for name, x, y, z, yaw in edge_corner_configs:
        edge_corner_nodes.append(
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                name=f'{name}_spawner',
                arguments=[
                    '-entity', name,
                    '-topic', 'robot_description',
                    '-x', str(x),
                    '-y', str(y),
                    '-z', str(z),
                    '-Y', str(yaw)
                ],
                parameters=[{'use_sim_time': True}],
                remappings=[('robot_description', 'edge_corner_description')]
            )
        )
    
    return LaunchDescription([
        declare_track_type,
        declare_barrier_type,
        declare_complexity,
        declare_size,
        spawn_world_launch,
        object_descriptions_launch
    ] + straight_nodes + corner_nodes + edge_straight_nodes + edge_corner_nodes)

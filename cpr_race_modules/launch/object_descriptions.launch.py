from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetParameter
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, TextSubstitution


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
    
    # Set parameters using xacro commands
    # These parameters will be available to spawn_entity nodes
    ground_description = SetParameter(
        name='ground_description',
        value=Command([
            'xacro ',
            PathJoinSubstitution([
                FindPackageShare('cpr_race_modules'),
                'urdf'
            ]),
            '/ground_',
            complexity,
            '.urdf.xacro'
        ])
    )
    
    edge_corner_description = SetParameter(
        name='edge_corner_description',
        value=Command([
            'xacro ',
            PathJoinSubstitution([
                FindPackageShare('cpr_race_modules'),
                'urdf'
            ]),
            '/',
            size,
            '_',
            barrier_type,
            '_edge_corner_',
            complexity,
            '.urdf.xacro'
        ])
    )
    
    edge_straight_description = SetParameter(
        name='edge_straight_description',
        value=Command([
            'xacro ',
            PathJoinSubstitution([
                FindPackageShare('cpr_race_modules'),
                'urdf'
            ]),
            '/',
            size,
            '_',
            barrier_type,
            '_edge_straight_',
            complexity,
            '.urdf.xacro'
        ])
    )
    
    corner_description = SetParameter(
        name='corner_description',
        value=Command([
            'xacro ',
            PathJoinSubstitution([
                FindPackageShare('cpr_race_modules'),
                'urdf'
            ]),
            '/',
            size,
            '_',
            track_type,
            '_corner_',
            complexity,
            '.urdf.xacro'
        ])
    )
    
    straight_description = SetParameter(
        name='straight_description',
        value=Command([
            'xacro ',
            PathJoinSubstitution([
                FindPackageShare('cpr_race_modules'),
                'urdf'
            ]),
            '/',
            size,
            '_',
            track_type,
            '_straight_',
            complexity,
            '.urdf.xacro'
        ])
    )
    
    return LaunchDescription([
        declare_track_type,
        declare_barrier_type,
        declare_complexity,
        declare_size,
        ground_description,
        edge_corner_description,
        edge_straight_description,
        corner_description,
        straight_description
    ])

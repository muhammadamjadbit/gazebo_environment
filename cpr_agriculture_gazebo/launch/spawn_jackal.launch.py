from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')
    yaw = LaunchConfiguration('yaw')
    
    declare_x = DeclareLaunchArgument('x', default_value='0.0')
    declare_y = DeclareLaunchArgument('y', default_value='-10.0')
    declare_z = DeclareLaunchArgument('z', default_value='5.0')
    declare_yaw = DeclareLaunchArgument('yaw', default_value='0.0')
    
    spawn_jackal = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('jackal_gazebo'),
                'launch',
                'spawn_jackal.launch.py'
            ])
        ]),
        launch_arguments={
            'x': x,
            'y': y,
            'z': z,
            'yaw': yaw
        }.items()
    )
    
    return LaunchDescription([
        declare_x,
        declare_y,
        declare_z,
        declare_yaw,
        spawn_jackal
    ])

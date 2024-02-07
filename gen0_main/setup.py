from setuptools import find_packages, setup
import os
from glob import glob


package_name = 'gen0_main'

# Iterate through all the files and subdirectories
# to build the data files array

data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ]


def package_files(data_files, directory_list):

    paths_dict = {}

    for directory in directory_list:

        for (path, directories, filenames) in os.walk(directory):

            for filename in filenames:

                file_path = os.path.join(path, filename)
                install_path = os.path.join('share', package_name, path)

                if install_path in paths_dict.keys():
                    paths_dict[install_path].append(file_path)

                else:
                    paths_dict[install_path] = [file_path]

    for key in paths_dict.keys():
        data_files.append((key, paths_dict[key]))

    return data_files

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files= package_files(data_files, ['launch/', 'worlds/', 'config/', 'urdf/', 'meshes/', 'models/']),
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='av-lab',
    maintainer_email='alkharrat.riyadh@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'odom_frame_corrector = gen0_main.odom_frame_corrector:main',
        'ground_truth_publisher = gen0_main.pose_publisher:main'
        ],
    },
)

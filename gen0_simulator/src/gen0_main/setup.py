from setuptools import find_packages, setup
import os
from glob import glob


package_name = 'gen0_main'

# Iterate through all the files and subdirectories
# to build the data files array

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
        glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'urdf'),
        glob(os.path.join('urdf', '*.*'))),
        (os.path.join('share', package_name, 'meshes'),
        glob(os.path.join('meshes', '*.*'))),
        (os.path.join('share', package_name, 'worlds/san_parking_model'),
        glob(os.path.join('worlds/**/*.*'))),
        (os.path.join('share', package_name, 'config'),
        glob(os.path.join('config', '*.*'))),
        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='av-lab',
    maintainer_email='alkharrat.riyadh@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)

from glob import glob
from setuptools import setup

setup(
    name='lab_py', version='1.0.0', packages=['lab_py'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/lab_py']),
        ('share/lab_py', ['package.xml']),
        ('share/lab_py/launch', glob('launch/*.launch.py')),
        ('share/lab_py/config', glob('config/*')),
        ('share/lab_py/worlds', glob('worlds/*')),
    ],
    install_requires=['setuptools'], zip_safe=True,
    maintainer='ROS 2 Course', maintainer_email='course@example.invalid',
    description='Curso ROS 2 en navegador', license='MIT',
    entry_points={'console_scripts': [
        'sensor = lab_py.sensor:main', 'rover = lab_py.rover:main',
        'patrol = lab_py.patrol:main', 'guard = lab_py.guard:main',
    ]},
)

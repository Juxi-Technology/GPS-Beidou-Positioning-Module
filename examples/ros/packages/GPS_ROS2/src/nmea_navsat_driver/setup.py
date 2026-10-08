from setuptools import setup

package_name = 'nmea_navsat_driver'

setup(
    name=package_name,
    version='0.5.0',
    packages=[package_name, package_name + '/nodes'],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ed Venator',
    maintainer_email='evenator@gmail.com',
    description='Package to parse NMEA strings and publish a very simple GPS message',
    license='BSD',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)

from setuptools import setup, find_packages

readme = open('README.md').read()

setup(
    name='mdslib',
    version="1.0",
    packages=find_packages(exclude=('test',)),
    url='https://github.com/Cisco-SAN/mdslib',
    license='',
    author="Cisco Systems, Inc.",
    author_email='subharad@cisco.com',
    description='Generic API/SDK library for Cisco MDS Switches',
    long_description=readme,
    install_requires=['requests', 'paramiko']
)

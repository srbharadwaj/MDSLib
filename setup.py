from setuptools import setup, find_packages

readme = open('README.md').read()

setup(
    name='MDSLIBRARY',
    version='',
    packages=find_packages(exclude=('test',)),
    url='https://github.com/srbharadwaj/mdsLib',
    license='',
    author='subharad',
    author_email='subharad@cisco.com',
    description='Generic API/SDK library for Cisco MDS Switches',
    long_description=readme,
    install_requires=['requests']
)
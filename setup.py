from setuptools import setup, find_packages

with open('requirements.txt') as rf:
    requirements = rf.readlines()

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

setup(
    name='mdslib',
    version="0.1.1",
    description='Generic Python SDK/API library for Cisco MDS Switches',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    author="Cisco Systems, Inc.",
    author_email='subharad@cisco.com',
    packages=find_packages(exclude=('test',)),
    url='https://github.com/Cisco-SAN/mdslib',
    license="http://www.apache.org/licenses/LICENSE-2.0",
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)

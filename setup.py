from setuptools import find_packages, setup

import os
import version 

# VERSION = version.get_version()

# __version__ = '2.2.1'
__version__ = version.get_version()

setup(
    name='django-dynamicschemas',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license='BSD license',
    description='For creating dynamic schemas with sqlite.',
    author='Bjarke Sporring',
    author_email='work.bjarke@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11.7',
        'Intended Audience :: Users',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    install_requires = [
        'jsonfield==2.0.2',
        'djangorestframework==3.7.3',
        ]
    )

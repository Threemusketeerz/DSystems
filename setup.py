import os
from setuptools import find_packages, setup

setup(
    name='django-dynamicschemas',
    version='2.2.0',
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

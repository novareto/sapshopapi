#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'zope.component',
    'zope.interface',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='sapshopapi',
    version='0.1.0',
    description="API for communicating with SAP-SHOP-API",
    long_description=readme + '\n\n' + history,
    author="Christian Klinger",
    author_email='ck@novareto.de',
    url='https://github.com/goschtl/sapshopapi',
    packages=[
        'sapshopapi',
    ],
    package_dir={'sapshopapi':
                 'sapshopapi'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='sapshopapi',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('INSTALL.rst') as installation_file:
    installation = installation_file.read()

with open('docs/usage.rst') as usage_file:
    usage = usage_file.read()

try:
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    requirements = [
        'defusedxml',
        'Click>=8.0.3',
        'scikit-learn>=1.3.0',
        'joblib',
        'rich',
        'pyyaml',
        'tomlkit',
    ]

try:
    with open('requirements_test.txt') as f:
        test_requirements = f.read().splitlines()
except FileNotFoundError:
    test_requirements = [
        'defusedxml',
        'Sphinx',
        'twine',
        'docutils',
        'pytest',
        'pytest-cov',
        'Click>=8.0.3',
        'lxml',
        'mypy',
    ]


setup_requirements = [
    'pytest-runner',
    'pytest',
    'pytest-cov',
]


setup(
    name='mlconjug3',
    version='3.11.0',
    description="A Python library to conjugate French, English, Spanish, Italian, Portuguese and Romanian verbs using Machine Learning techniques.",
    long_description=readme,
    long_description_content_type="text/x-rst",
    author="Ars-Linguistica",
    author_email='diao.sekou.nlp@gmail.com',
    url='https://github.com/Ars-Linguistica/mlconjug3',
    packages=find_packages(include=['mlconjug3']),
    entry_points={
        'console_scripts': [
            'mlconjug3=mlconjug3.cli:main'
        ]
    },
    package_data={'conjug_manager': ['mlconjug3/data/conjug_manager/*'],
                  'documentation': ['docs/*'],
                  'tests': ['tests/*'],
                  'trained_models': ['mlconjug3/data/models/*'],
                  'translations': ['mlconjug3/locale/*'],
                  'type_stubs': ['mlconjug3/py.typed', 'mlconjug3/*'],
                  'requirements': ['requirements.txt',
                                   'requirements_dev.txt',
                                   'requirements_test.txt']
                  },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='mlconjug3 conjugate conjugator conjugation conjugaison conjugación coniugazione conjugação conjugare'
             ' verbs verbes verbos ML machine-learning NLP linguistics linguistique linguistica conjug_manager sklearn'
             'scikit-learn',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: French',
        'Natural Language :: Spanish',
        'Natural Language :: Italian',
        'Natural Language :: Portuguese',
        'Natural Language :: Romanian',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)

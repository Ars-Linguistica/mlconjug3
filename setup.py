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

requirements = [
    'cython',
    'Click>=6.0',
    'numpy',
    'scipy',
    'scikit-learn>=0.20.2',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
    'Sphinx',
    'docutils',
    'pytest',
    'pytest-cov',
    'Click>=6.0',
    'lxml',
    'mypy',
]

setup(
    name='mlconjug',
    version='3.4.0',
    description="A Python library to conjugate French, English, Spanish, Italian, Portuguese and Romanian verbs using Machine Learning techniques.",
    long_description=readme + '\n\n' + installation + '\n\n' + usage + '\n\n' + history,
    author="SekouD",
    author_email='sekoud.python@gmail.com',
    url='https://github.com/SekouD/mlconjug',
    packages=find_packages(include=['mlconjug']),
    entry_points={
        'console_scripts': [
            'mlconjug=mlconjug.cli:main'
        ]
    },
    package_data={'conjug_manager': ['mlconjug/data/conjug_manager/*'],
                  'documentation': ['docs/*'],
                  'tests': ['tests/*'],
                  'trained_models': ['mlconjug/data/models/*'],
                  'translations': ['mlconjug/locale/*'],
                  'type_stubs': ['mlconjug/py.typed', 'mlconjug/*']},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='mlconjug conjugate conjugator conjugation conjugaison conjugación coniugazione conjugação conjugare'
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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)

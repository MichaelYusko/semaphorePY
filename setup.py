import semaphore

from setuptools import setup

setup_parameters = {
    'name': 'semaphorePY',
    'author': semaphore.__author__,
    'version': semaphore.__version__,
    'license': 'MIT',
    'author_email': 'mikeiceman1221@gmail.com',
    'description': 'SemaphoreCI python wrapper',
    'packages': ['semaphore'],
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License'
    ],
}


requirements = ['requests>=2.19.1']

setup_parameters['install_requires'] = requirements

setup(**setup_parameters)

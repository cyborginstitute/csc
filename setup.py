from setuptools import setup

setup(
    name='',
    description='A framework for genarting static websites with reStructuredtext.',
    version='0.1.dev',
    license='Apache',
    url='http://cyborginstitute.org/projects/csc',
    packages=['csc'],
    test_suite=None
    entry_points={
        'console_scripts': [
            'csc = csc.csc:main',
            'csa = csc.csa:main',
            ],
        }
    )

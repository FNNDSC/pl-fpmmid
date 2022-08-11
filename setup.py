from os import path
from setuptools import setup

setup(
    name='fpmmid',
    version='1.0.5',
    description='A ChRIS DS plugin template',
    author='FNNDSC',
    author_email='dev@babyMRI.org',
    url='https://github.com/FNNDSC/pl-fpmmid',
    py_modules=['fpmmid'],
    packages   = ['fpmmid','model','scripts.run','scripts.run.modules'],
    install_requires=['chrisapp'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license='MIT',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points={
        'console_scripts': [
            'fpmmid = fpmmid.fpmmid:main'
        ]
    }

)

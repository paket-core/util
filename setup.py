"""Install PaKeT Project general utils."""
from setuptools import setup

setup(name='util',
      description='General utilities for PaKeT project',
      version='1.0.0',
      url='https://github.com/paket-core/util',
      license='GNU GPL',
      packages=['util'],
      install_requires=[
          'coloredlogs==10.0',
          'requests==2.18.4'
      ],
      test_suite='tests',
      zip_safe=False)
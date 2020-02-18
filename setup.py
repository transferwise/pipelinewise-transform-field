#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pipelinewise-transform-field',
      version='1.2.0',
      description='Singer.io simple field transformator between taps and targets - PipelineWise compatible',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author="TransferWise",
      url='https://github.com/transferwise/pipelinewise-transform-field',
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3 :: Only'
      ],
      py_modules=['transform_field'],
      install_requires=[
          'pipelinewise-singer-python==1.*',
      ],
      entry_points='''
          [console_scripts]
          transform-field=transform_field:main
      ''',
      packages=['transform_field']
)

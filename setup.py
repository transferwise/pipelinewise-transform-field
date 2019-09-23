
#!/usr/bin/env python

from setuptools import setup

setup(name='pipelinewise-transform-field',
      version='1.1.1',
      description='Singer.io simple field transformator between taps and targets - PipelineWise compatible',
      author="TransferWise",
      url='https://github.com/transferwise/pipelinewise-transform-field',
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3 :: Only'
      ],
      py_modules=['transform_field'],
      install_requires=[
          'singer-python==5.2.0',
      ],
      entry_points='''
          [console_scripts]
          transform-field=transform_field:main
      ''',
      packages=['transform_field']
)

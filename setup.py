#!/usr/bin/env python
from distutils.core import setup

MAJOR = 0
MINOR = 3
BUILD = 3

version = "%s.%s" % (MAJOR, MINOR)
release = "%s.%s.%s" % (MAJOR, MINOR, BUILD)

setup(name='yaml2dataclass',
      version=release,
      description='Load type annotated dataclasses from YAML files.',
      long_description="A little helper class that lets you load type annotated dataclasses from YAML files. "
                       "Supports nested data structures.",
      author='László Zsolt Nagy',
      author_email='nagylzs@gmail.com',
      license="http://www.apache.org/licenses/LICENSE-2.0",
      packages=['yaml2dataclass'],
      install_requires=['pyyaml'],
      url="https://github.com/nagylzs/yaml2dataclass",
      classifiers=[
          "Topic :: Utilities",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: Implementation :: CPython",
          "Operating System :: Microsoft :: Windows",
          "Operating System :: Unix",
      ],
      )

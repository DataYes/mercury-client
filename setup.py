# -*- coding: utf-8 -*-
NAME = 'Mercury-Client'
VERSION = '0.1'
AUTHORS = 'taotao.li'
MAINTAINER = 'taotao.li'
EMAIL = 'taotao.li@datayes.com'
URL = 'q.datayes.com'
LICENSE = 'GPL'


import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
      name = NAME,
      description = 'Package for Datayes Mercury API access',
      long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
      version = VERSION,
      author = ", ".join(AUTHORS),
      maintainer = MAINTAINER,
      maintainer_email = EMAIL,
      url = URL,
      license = LICENSE,
      install_requires = [
        "requests >= 2.5.1",
      ],
      packages = ['mercury']
)
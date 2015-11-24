# -*- coding: utf-8 -*-
"""
This module contains the tool of collective.recipe.buildoutcache
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0.3'

long_description = (
    read('README.rst')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.rst')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.rst')
    + '\n' +
    'Download\n'
    '********\n')

entry_point = 'collective.recipe.buildoutcache:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

tests_require = [
    'zope.testing',
    'plone.testing',
    'unittest2',
    'zc.buildout']

setup(name='collective.recipe.buildoutcache',
      version=version,
      description="Recipe for generate buildout-cache.tar.gz2",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Framework :: Buildout',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
      ],
      keywords='Plone Buildout Recipe Buildout-Cache Python',
      author='Benoît Suttor',
      author_email='bsuttor@imio.be',
      url='https://github.com/collective/collective.recipe.buildoutcache',
      license='gpl',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout'
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='collective.recipe.buildoutcache.tests.test_docs.test_suite',
      entry_points=entry_points,
      )

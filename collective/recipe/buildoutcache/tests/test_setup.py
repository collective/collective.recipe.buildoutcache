# -*- coding: utf-8 -*-
from collective.recipe.buildoutcache.testing import RECIPE_FIXTURE
from unittest2 import TestCase
import os


BUILDOUT_CONFIG = '\n'.join((
    '[buildout]',
    'parts = makebuildoutcachetgz',
    '',
    '[makebuildoutcachetgz]',
    'recipe = collective.recipe.buildoutcache'))


class TestSetup(TestCase):

    layer = RECIPE_FIXTURE

    def setUp(self):
        self.__dict__.update(self.layer['buildout'])
        self.maxDiff = None

    def test_installing_recipe(self):
        self.write('buildout.cfg', BUILDOUT_CONFIG)
        output = self.system(self.buildout).strip()
        self.assertRegexpMatches(output, r'^Installing makebuildoutcachetgz')
        self.assertRegexpMatches(output,
                                 r'Generated script.*bin/makebuildoutcachetgz')

    def test_recipe_creates_script(self):
        self.write('buildout.cfg', BUILDOUT_CONFIG)
        self.system(self.buildout)
        expected = os.path.join(self.sample_buildout, 'bin', 'makebuildoutcachetgz')
        self.assertTrue(os.path.exists(expected),
                        'Missing executable %s' % expected)

    def test_script_is_executable(self):
        self.write('buildout.cfg', BUILDOUT_CONFIG)
        self.system(self.buildout)
        path = os.path.join(self.sample_buildout, 'bin', 'makebuildoutcachetgz')
        self.assertTrue(os.access(path, os.X_OK),
                        '%s should be executable' % path)


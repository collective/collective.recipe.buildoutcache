# -*- coding: utf-8 -*-
from collective.recipe.buildoutcache.testing import RECIPE_FIXTURE
from collective.recipe.buildoutcache.run import do_command
from collective.recipe.buildoutcache.run import bin_buildout
from collective.recipe.buildoutcache.run import prepare_cache
from unittest2 import TestCase
import os


BUILDOUT_CONFIG = '\n'.join((
    '[buildout]',
    'parts = makebuildoutcachetgz',
    '',
    '[makebuildoutcachetgz]',
    'recipe = collective.recipe.buildoutcache'))


class TestRun(TestCase):

    layer = RECIPE_FIXTURE

    def setUp(self):
        self.__dict__.update(self.layer['buildout'])
        # self.maxDiff = None
        self.write('buildout.cfg', BUILDOUT_CONFIG)
        self.system(self.buildout)
        self.project_dir = os.sep.join(self.buildout.split(os.sep)[:-2])

    def test_use_script(self):
        self.script = "{0}/bin/makebuildoutcachetgz".format(self.project_dir)
        do_command(self.script)
        self.assertTrue(os.path.exists('{0}/buildout-cache.tar.bz2'.format(self.project_dir)))

    def test_bin_buildout(self):
        self.assertFalse(os.path.exists('{0}/tmp/buildout-cache/downloads/dist'.format(self.project_dir)))
        buildoutcache_dir = "{0}/tmp/buildout-cache".format(self.project_dir)
        bin_buildout(
            buildout_file='buildout.cfg',
            buildoutcache_dir=buildoutcache_dir,
            buildout_dir=self.project_dir)
        self.assertTrue(os.path.exists('{0}/tmp/buildout-cache/downloads/dist'.format(self.project_dir)))

    def test_prepare_cache(self):
        buildoutcache_dir = "{0}/tmp/buildout-cache".format(self.project_dir)
        bin_buildout(
            buildout_file='buildout.cfg',
            buildoutcache_dir=buildoutcache_dir,
            buildout_dir=self.project_dir)
        self.assertRegexpMatches(prepare_cache(buildoutcache_dir),
                                 r'collective.recipe.buildoutcache: Removing installed eggs with binary components:')


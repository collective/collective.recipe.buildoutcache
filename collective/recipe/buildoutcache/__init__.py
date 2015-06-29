# -*- coding: utf-8 -*-
"""Recipe buildoutcache"""
from zc.buildout.easy_install import scripts as create_script
from pkg_resources import working_set
from sys import executable


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        if 'target' in self.options:
            self.target = options['target']
        else:
            self.target = 'buildout-cache.tar.bz2'
        if 'buildout_file' in self.options:
            self.buildout_file = options['buildout_file']
        else:
            self.buildout_file = 'buildout.cfg'
        if 'work_dir' in self.options:
            self.work_dir = options['work_dir']
        else:
            self.work_dir = 'tmp'

    def install(self):
        """Installer"""
        # XXX Implement recipe functionality here
        bindir = self.buildout['buildout']['bin-directory']
        arguments = ''
        for key, value in {
            'target': self.target,
            'buildout_file': self.buildout_file,
            'work_dir': self.work_dir
        }.iteritems():
            if value is not None:
                arguments += "%s='%s', " % (key, value)
        create_script(
            [
                (
                    '%s' % self.name,
                    'collective.recipe.buildoutcache.run', 'maketargz')
            ],
            working_set,
            executable,
            bindir,
            arguments=arguments)
        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return tuple()

    def update(self):
        """Updater"""
        self.install()

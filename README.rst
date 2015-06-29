.. contents::

Introduction
============

This recipe is used to generate buildout-cache.tar.gz2 file.

The recipe was inspired by update-packages script from Plone Installers-UnifiedInstaller (https://github.com/plone/Installers-UnifiedInstaller/blob/master/update_packages.py)
The recipe will start a buildout with forced eggs-directory and download-cache. After it will deleted eggs with binary components, make some cleanup, and finally generate compressed file contains buildout-cache.


Supported options
=================

The recipe supports the following optionnal options:

.. Note to recipe author!
   ----------------------
   For each option the recipe uses you should include a description
   about the purpose of the option, the format and semantics of the
   values it accepts, whether it is mandatory or optional and what the
   default value is if it is omitted.


target
    Name of target compressed file. Default value is `buildout-cache.tar.bz2`.

buildout_file
    Name of buildout file which be used for constuction of buildout cache. Default value is `buildout.cfg`.

work_dir
    Directory where eggs are downloaded for creation of tar.gz2 file. This directroy is deleted before and after the script. Default value is `tmp`.


Example usage
=============

We'll start by creating a `buildout.cfg` file that uses the recipe::

    [buildout]
    parts = makebuildoutcache

    [makebuildoutcache]
    recipe = collective.recipe.buildoutcache

    target = buildout-cache.tar.bz2
    buildout_file = buildout.cfg
    work_dir = my-temp-buildout-work-dir

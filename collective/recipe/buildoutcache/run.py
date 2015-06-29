import subprocess
import os
import re
import shutil
import logging
from collective.recipe.buildoutcache.package_list import PackageList
FORMAT = '%(asctime)s :: collective.recipe.buildoutcache :: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('collective.recipe.buildoutcache')
logger.setLevel(logging.INFO)

BINARY_SIG_RE = re.compile(r'-py2.[7]-.+(?=.egg)')
PY_SIG = '-.py2.7'


def do_command(cmd):
    po = subprocess.Popen(cmd,
                          shell=True,
                          universal_newlines=True)
    po.communicate()


def maketargz(target='buildout-cache.tar.bz2', buildout_file='buildout.cfg', work_dir='tmp', buildout_dir='.'):
    complete_work_dir = "{0}/{1}".format(buildout_dir, work_dir)
    if os.path.exists(complete_work_dir):
        logger.info('Remove existing work dir')
        shutil.rmtree(complete_work_dir)
    buildoutcache_dir = '{0}/buildout-cache'.format(complete_work_dir)

    bin_buildout(buildout_file, buildoutcache_dir, buildout_dir)
    prepare_cache(buildoutcache_dir)
    make_archive(target, work_dir)


def bin_buildout(buildout_file, buildoutcache_dir, buildout_dir='.'):
    logger.info('Create tmp folder for buildout cache downloads')
    do_command('mkdir -p {0}/downloads'.format(buildoutcache_dir))

    logger.info('Starting buildout...')
    cmd = '{2}/bin/buildout -Nt 7 -c {0} buildout:eggs-directory={1}/eggs buildout:download-cache={1}/downloads'.format(buildout_file, buildoutcache_dir, buildout_dir)
    do_command(cmd)


def prepare_cache(buildoutcache_dir):
    eggs = os.path.join(buildoutcache_dir, 'eggs')
    downloads = os.path.join(buildoutcache_dir, 'downloads')
    dist = os.path.join(downloads, 'dist')

    packages = PackageList((dist, ))
    packages.clean_older()
    packages = PackageList((eggs, ))
    packages.clean_older()

    binaries = {}

    logger.info('Removing installed eggs with binary components:')
    for fn in os.listdir(eggs):
        if BINARY_SIG_RE.search(fn) is not None:
            basename = BINARY_SIG_RE.sub('', fn).replace('.egg', '')
            binaries[basename] = 1
            shutil.rmtree(os.path.join(eggs, fn))
            logger.info(basename,)

    logger.info('Removing dist packages without binary components. Remaining:')
    for fn in os.listdir(dist):
        basename = BINARY_SIG_RE.sub('', fn).replace('.tar.gz', '').replace('.zip', '')
        if basename in binaries:
            del binaries[basename]
            logger.info(basename)
        else:
            os.unlink(os.path.join(dist, fn))

    if binaries:
        logger.error("Ooops: {0}".format(binaries.keys()))

    logger.info('zap *.py[c|o] files from installed eggs')
    do_command("find %s -name '*.py[co]' -exec rm {} \\;" % eggs)
    logger.info('zap *.mo files from installed eggs')
    do_command("find %s -name '*.mo' -exec rm {} \\;" % eggs)

    logger.info('Removing .registration.cache files')
    do_command("find %s -name '.registration.cache' -exec rm {} \\;" % eggs)

    # clean mac crapola
    do_command('find %s -name ".DS_Store" -exec rm {} \;' % buildoutcache_dir)

    logger.info("permission fixups")
    do_command("find %s -type d -exec chmod 755 {} \;" % buildoutcache_dir)
    do_command("find %s -type f -exec chmod 644 {} \;" % buildoutcache_dir)


def make_archive(target, work_dir):
    if os.path.exists(target):
        logger.info('remove existing buildout cache archive')
        os.unlink(target)
    # GNU tar is required for this task...
    # BSD tar does not have the same set of options that we require.
    # Does the system have 'tar' set or symlinked to gnutar?
    p = subprocess.Popen(['tar', '--version'], stdout=subprocess.PIPE)
    stdout = p.communicate()[0]
    has_gnutar = False
    if stdout.find('GNU') >= 0:
        has_gnutar = True
        tar_command = 'tar'
    else:
        # Check for the existance of the 'gnutar' command.
        rcode = subprocess.call(['which', 'gnutar'])
        if rcode == 0:
            has_gnutar = True
            tar_command = 'gnutar'
    if not has_gnutar:
        raise RuntimeError("GNU tar is required to complete this packaging.")

    # generate new archive
    cmd = "{0} --owner 0 --group 0 --exclude=.DS_Store -jcf {1} -C {2} buildout-cache".format(tar_command, target, work_dir)
    do_command(cmd)

    logger.info('Delete tmp folder for buildout cache downloads')
    do_command('rm -rf {0}'.format(work_dir))

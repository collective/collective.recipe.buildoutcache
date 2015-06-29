import os.path
import re
import pkg_resources
import shutil

BINARY_SIG_RE = re.compile(r'-py2.[7]-.+(?=.egg)')
PY_SIG = '-.py2.7'


class PackageList:

    pkgpat = re.compile(r'(.+)-(\d.+?)\.(?:zip|egg|tar|tar.gz|tgz)$')

    def __init__(self, pathnames):
        self.packages = {}

        for pathname in pathnames:
            for fn in os.listdir(pathname):
                basename = BINARY_SIG_RE.sub('', fn).replace(PY_SIG, '')
                mo = self.pkgpat.match(basename)
                if mo:
                    name, version = mo.groups()[0:2]
                    self.packages.setdefault(name, []).append((
                        pkg_resources.parse_version(version),
                        os.path.join(pathname, fn)))

    def older_versions(self):
        for eggk in self.packages.keys():
            eggv = self.packages[eggk]
            if len(eggv) > 1:
                eggv.sort()
                for i in range(0, len(eggv) - 1):
                    yield eggv[i][1]

    def clean_older(self):
        for fn in self.older_versions():
            if os.path.isdir(fn):
                shutil.rmtree(fn)
            else:
                os.unlink(fn)

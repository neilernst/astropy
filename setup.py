#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst

import glob
import os
import sys

import ah_bootstrap
from setuptools import setup

from astropy_helpers.setup_helpers import (
    register_commands, get_package_info, get_debug_option)
try:
    from astropy_helpers.distutils_helpers import is_distutils_display_option
except:
    # For astropy-helpers v0.4.x
    from astropy_helpers.setup_helpers import is_distutils_display_option
from astropy_helpers.git_helpers import get_git_devstr
from astropy_helpers.version_helpers import generate_version_py

import astropy

NAME = 'astropy'

# VERSION should be PEP386 compatible (http://www.python.org/dev/peps/pep-0386)
VERSION = '2.0.dev'

# Indicates if this version is a release version
RELEASE = 'dev' not in VERSION

if not RELEASE:
    VERSION += get_git_devstr(False)

# Populate the dict of setup command overrides; this should be done before
# invoking any other functionality from distutils since it can potentially
# modify distutils' behavior.
cmdclassd = register_commands(NAME, VERSION, RELEASE)

# Freeze build information in version.py
generate_version_py(NAME, VERSION, RELEASE, get_debug_option(NAME),
                    uses_git=not RELEASE)

# Get configuration information from all of the various subpackages.
# See the docstring for setup_helpers.update_package_files for more
# details.
package_info = get_package_info()

# Add the project-global data
package_info['package_data'].setdefault('astropy', []).append('data/*')

# Add any necessary entry points
entry_points = {}
# Command-line scripts
entry_points['console_scripts'] = [
    'fits2bitmap = astropy.visualization.scripts.fits2bitmap:main',
    'fitscheck = astropy.io.fits.scripts.fitscheck:main',
    'fitsdiff = astropy.io.fits.scripts.fitsdiff:main',
    'fitsheader = astropy.io.fits.scripts.fitsheader:main',
    'fitsinfo = astropy.io.fits.scripts.fitsinfo:main',
    'samp_hub = astropy.vo.samp.hub_script:hub_script',
    'volint = astropy.io.votable.volint:main',
    'wcslint = astropy.wcs.wcslint:main',
]

setup_requires = ['numpy>=' + astropy.__minimum_numpy_version__]
install_requires = ['pytest>=2.8', 'numpy>=' + astropy.__minimum_numpy_version__]
# Avoid installing setup_requires dependencies if the user just
# queries for information
if is_distutils_display_option():
    setup_requires = []


setup(name=NAME,
      version=VERSION,
      description='Community-developed python astronomy tools',
      requires=['numpy'],  # scipy not required, but strongly recommended
      setup_requires=setup_requires,
      install_requires=install_requires,
      provides=[NAME],
      author='The Astropy Developers',
      author_email='astropy.team@gmail.com',
      license='BSD',
      url='http://astropy.org',
      long_description=astropy.__doc__,
      keywords=['astronomy', 'astrophysics', 'cosmology', 'space', 'science',
                'units', 'table', 'wcs', 'vo', 'samp', 'coordinate', 'fits',
                'modeling', 'models', 'fitting', 'ascii'],
      classifiers=[
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: C',
          'Programming Language :: Cython',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Topic :: Scientific/Engineering :: Physics'
      ],
      cmdclass=cmdclassd,
      zip_safe=False,
      use_2to3=False,
      entry_points=entry_points,
      python_requires='>=2.7',
      **package_info
)

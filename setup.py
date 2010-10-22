#!/usr/bin/env python
"""
py2app/py2exe build script for MyApplication.

Will automatically ensure that all build prerequisites are available
via ez_setup

Usage (Mac OS X):
    python setup.py py2app

Usage (Windows):
    python setup.py py2exe

Usage (Ubuntu/Debian):
    python setup.py --command-packages=stdeb.command bdist_deb

Usage (RPM-based linux distros):
    python setup.py bdist_rpm
"""
import glob
from distutils.core import setup
import sys

mainscript = 'src/cryotec_client.pyw'

base_options = dict (name='cryotec_client',
      install_requires = ["qtdjango","pyqt"],
      version='1.0',
      description='Cryotec Client',
      author='Sergey Klimov',
      author_email='dcdarv@gmail.com',
      url='http://github.com/darvin/cryotec_client',
      package_dir = {'cryotec_client': 'src'},
      packages=['cryotec_client'],

      #data_files=[('share/pythonturtle',glob.glob('data/*.png')),
#                  ('share/pythonturtle',glob.glob('data/*.ico')),
#  ],
      long_description="""Cryotec Client""",
      license="Greedy Open Source",
      maintainer="Sergey Klimov",
      maintainer_email="dcdarv@gmail.com",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          ],
      #cmdclass = { "build" : build_extra.build_extra,
               #"build_i18n" :  build_i18n.build_i18n,
               #"build_help" :  build_help.build_help,
      #         "build_icons" :  build_icons.build_icons }
      
     )



if sys.platform == 'darwin':
    extra_options = dict(
        setup_requires=['py2app'],
        app=[mainscript],
        # Cross-platform applications generally expect sys.argv to
        # be used for opening files.
        options=dict(py2app=dict(argv_emulation=True)),

    )
elif sys.platform == 'win32':

    import sys

    sys.path.append(r'c:/Program Files/Microsoft Visual Studio 9.0/VC/redist/x86/Microsoft.VC90.CRT')
    sys.path.append(r'c:\Python27\vcruntime')
    
    import py2exe
    extra_options = dict(
        setup_requires=['py2exe'],
        windows=[mainscript],
        options = {
            py2exe : {
                "includes" : ["sip", "PyQt4._qt"]
                }
            },
        data_files = [('resources',glob.glob('data/*.png')),
                      ('resources',glob.glob('data/*.ico')),
                      ("Microsoft.VC90.CRT", glob.glob(r'c:\Python27\vcruntime\*.*'))],

    )
else:
     extra_options = dict(
         # Normally unix-like platforms will use "setup.py install"
         # and install the main script as such
         scripts=[mainscript],
      )


base_options.update(extra_options)
options = base_options 



setup( **options)

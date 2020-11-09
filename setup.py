#from distutils.core import setup
from setuptools import setup
#import glob, os, re, sys
#import setuptools; setuptools.bootstrap_install_from = egg
#from setuptools import Extension, find_packages, setup
# read the contents of your README file


exec(open('un0usb/version.py').read())

setup(
  name = 'un0usb',         # How you named your package folder (MyLib)
  packages = ['un0usb'],   # Chose the same as "name"
  version = __version__,      # Start with a small number and increase it with every change you make
  license='gpl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Library for un0rick usb interface',   # Give a short description about your library
  author = 'Luc Jonveaux',                   # Type in your name
  author_email = 'kelu124@gmail.com',      # Type in your E-Mail
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  url = 'http://un0rick.cc',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/kelu124/python-usb-un0rick/archive/v0.2.1.tar.gz',    # I explain this later on
  keywords = ['ultrasound', 'usb', 'un0rick'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pyftdi','numpy','matplotlib',
          ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Science/Research',      # Define that your audience are developers
    'Topic :: Scientific/Engineering :: Physics',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
  zip_safe=False,
  include_package_data=True, 
  data_files=[('firmware',['usb.bin',"README.md"]),],
)

import multiprocessing
import os
from setuptools import setup
import subprocess
import sys
from distutils.command.build import build as DistutilsBuild
import distutils

class Build(DistutilsBuild):
    def run(self):
        cores_to_use = max(1, multiprocessing.cpu_count()-1)
        try:
            subprocess.check_call(['git', 'clone', 'git@github.com:LARG/HFO.git', 'hfo_py'])
            subprocess.check_call(['cmake','-DCMAKE_BUILD_TYPE=Release'], cwd='hfo_py')
            subprocess.check_call(['make', 'install', '-j', str(cores_to_use)], cwd='hfo_py')
        except subprocess.CalledProcessError as e:
            sys.stderr.write("Could not build hfo-py: %s.\n" % e)
            raise
        DistutilsBuild.run(self)

if not os.path.exists('hfo_py'):
    os.makedirs('hfo_py')

setup(name='hfo-py',
      version='0.1',
      author='Matthew Hausknecht',
      author_email='matthew.hausknecht@gmail.com',
      description='Half Field Offense in 2D RoboCup Soccer.',
      packages=['hfo_py'],
      cmdclass={'build': Build },
      include_package_data=True
)

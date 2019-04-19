import os
from setuptools import setup, find_packages


def version():

    setup_dir = os.path.dirname(os.path.realpath(__file__))
    version_file = open(os.path.join(setup_dir, 'Binning_refiner', 'VERSION'))

    return version_file.readline().strip()


__long_description__ = '''

Binning_refiner: Improving genome bins through the combination of different binning programs

Weizhi Song (songwz03@gmail.com)

The Centre for Marine Bio-Innovation (CMB), 
University of New South Wales, Sydney, Australia

'''


setup(name="Binning_refiner",
      version=version(),
      long_description=__long_description__,
      license="GPL3+",
      author="Weizhi Song, Torsten Thomas",
      author_email="songwz03@gmail.com",
      keywords="Bioinformatics Metagenomics Binning Refinement",
      description="Binning_refiner",
      url="https://github.com/songweizhi/Binning_refiner",
      packages=['Binning_refiner'],
      package_data={'': ['*.r', '*.R', '*.py', 'VERSION']},
      include_package_data=True,
      install_requires=['biopython'],
      scripts=['bin/Binning_refiner'])


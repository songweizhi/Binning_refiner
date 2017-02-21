from setuptools import setup, find_packages
import sys, os, shutil

with open('README.md') as readme_file:
    readme = readme_file.read()

__version__ = "1.1"

def recursive_find(directory):
    """List the files in a directory recursively, sort of like Unix 'find'"""
    file_list = []
    for root, _, files in os.walk(directory):
        for f in files:
            file_list.append(os.path.join(root,f))
            if len(file_list) > 300:
                raise Exception("Too many files added to the recursive list")
    return file_list

setup(
    name='Binning_refiner',
    version=__version__,
    description='Improve genome bins through the combination of different binning programs',
    long_description=readme,
    url="https://github.com/songweizhi/Binning_refiner",
    author='Weizhi Song, Torsten Thomas',
    license='GPL3+',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ],
    keywords="metagenomics bioinformatics",
    packages=find_packages(exclude=['contrib','docs']),
    install_requires=('rpy2',
                      'biopython',
                      'matplotlib',
                      'numpy'),
    scripts=['bin/Binning_refiner',
             'bin/CheckM_runner',
             'bin/Get_statistics']
)

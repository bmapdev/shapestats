#! /usr/local/epd/bin/python
__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2013, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "s.joshi@ucla.edu"
__credits__ = 'Inspired by the stats package rshape by Roger P. Woods'


from distutils.core import setup
# from setuptools import setup
base_dir = 'shapestats'
setup(
    name='shapestats',
    version='0.1dev',
    packages=['shapestats'],
    package_dir={'shapestats': base_dir, },
    test_suite='nose.collector',
    scripts=['bin/shapestats.py', 'bin/paired_t_test_shape.py'],
    license='MIT/TBD',
    exclude_package_data={'': ['.gitignore', '.idea']},
    author='Shantanu H. Joshi, David Shattuck, Roger P. Woods',
    author_email='s.joshi@ucla.edu, shattuck@ucla.edu, rwoods@ucla.edu',
    __credits__='Contributions and ideas: Shantanu H. Joshi, David Shattuck, Roger P. Woods'
                'Inspired by the stats package rshape by Roger P. Woods',
    description='shape statistics package',
    # install_requires=[
    #     "numpy",
    #     "pandas",
    #     "statsmodels",
    #     "rpy2",
    # ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: MIT/TBD',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    keywords='shape statistics',
)

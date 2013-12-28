#! /usr/local/epd/bin/python

"""Output specification for statistical tests"""

__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2013, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "s.joshi@ucla.edu"
__credits__ = 'Inspired by the stats package rshape by Roger P. Woods'

import numpy as np
import os
from shapeio.shape import Shape
import sys


class StatsOutput(object):

    def __init__(self, dim=0):
        self.pvalues = np.zeros(dim)
        self.pvalues_signed = np.zeros(dim)
        self.tvalues = np.zeros(dim)

    def save(self, outdir, outprefix, statsdata, atlas_filename=None, shape_average=None):

        if not atlas_filename and not shape_average:
            sys.stdout.write('Error: Either atlas shape file or a coordinate shape average has to be provided.\n')
            sys.stdout.write('Quitting without saving output.')
            return
        else:
            if atlas_filename and shape_average:  #Both are provided. Use the atlas
                shape_average = None

            if atlas_filename:
                s1 = Shape.readfile(atlas_filename)
                s1.attributes = self.pvalues
                if len(s1.attributes) != s1.coords.shape[0]:
                    sys.stdout.write('Error: Dimension mismatch between the p-values and the number of vertices. '
                                     'Quitting without saving.\n')
                Shape.writefile(os.path.join(outdir, outprefix + '_pvalues' + statsdata.filext), s1)
                return

            if shape_average:
                s1 = shape_average
                s1.attributes = self.pvalues


        # print s1.attributes


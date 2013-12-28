#! /usr/local/epd/bin/python

"""Class for performing multiple testing (comparisons)"""

__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2013, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "s.joshi@ucla.edu"
__credits__ = 'Inspired by the stats package rshape by Roger P. Woods'

from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
import numpy as np
stats = importr('stats')


class Stats_Multi_Comparisons():

    def __init__(self):
        pass

    @staticmethod
    def adjust(pvalues, method='BH'):
        direction = np.sign(pvalues)
        p_adjust = stats.p_adjust(FloatVector(np.abs(pvalues)), method=method)
        return p_adjust*direction


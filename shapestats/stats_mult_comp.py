#! /usr/local/epd/bin/python

"""Class for performing multiple testing (comparisons)"""

__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2013, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "s.joshi@ucla.edu"
__credits__ = 'Inspired by the stats package rshape by Roger P. Woods'

import numpy as np
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
stats = importr('stats')


class Stats_Multi_Comparisons():

    def __init__(self):
        pass

    @staticmethod
    def adjust(pvalues, method='BH', alpha=0.05, maskfile=None):

        p_adjust = pvalues
        direction = np.ones(len(pvalues))
        if maskfile:
            mask_idx = np.loadtxt(maskfile, np.dtype(int), delimiter='\n')

            valid_idx = list(set(range(len(pvalues))) - set(mask_idx))
            direction_mask = np.sign(pvalues[valid_idx])
            p_adjust_mask = stats.p_adjust(FloatVector(np.abs(pvalues)), method=method)
            p_adjust[valid_idx] = p_adjust_mask
            p_adjust[mask_idx] = 1
            direction[valid_idx] = direction_mask
            direction[mask_idx] = 1
        else:
            direction = np.sign(pvalues)
            p_adjust = stats.p_adjust(FloatVector(np.abs(pvalues)), method=method)

        return p_adjust*direction

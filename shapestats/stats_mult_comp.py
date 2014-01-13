#! /usr/local/epd/bin/python

"""Class for performing multiple testing (comparisons)"""

__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2013, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "s.joshi@ucla.edu"
__credits__ = 'Inspired by the stats package rshape by Roger P. Woods'

import numpy as np
from statsmodels.sandbox.stats.multicomp import multipletests


class Stats_Multi_Comparisons():

    def __init__(self):
        pass

    @staticmethod
    def adjust(pvalues, method='fdr_tsbh', alpha=0.05):
        direction = np.sign(pvalues)
        rejected_pvalues, p_adjust, alphacSidak, alphacBonf = \
            multipletests(np.abs(pvalues), alpha=alpha, method=method)
        return p_adjust*direction


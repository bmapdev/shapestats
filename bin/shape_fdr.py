#!/usr/bin/env python
"""
Correct p-values for multiple comparisons using using fdr
"""

__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2013, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "s.joshi@ucla.edu"

import argparse
from shapeio.shape import Shape
from shapestats.stats_mult_comp import Stats_Multi_Comparisons
from shapestats.colormaps import Colormap
import numpy as np


def main():
    parser = argparse.ArgumentParser(description='Adjust p-values by testing for multiple comparisons using fdr.\n')
    parser.add_argument('shapein', help='input surface/curve with p-values as attributes')
    parser.add_argument('shapeout', help='output surface/curve with fdr corrected p-values as attributes')
    parser.add_argument('-method', dest='method', help='correction method - one of the following: bonferroni, BH, BY, holm, hochberg',
                        required=False, default='BH')
    parser.add_argument('-mask', dest='mask', help='text file of indices to be masked', required=False, default=None)
    parser.add_argument('-q', dest='alpha', help='FDR threshold', type=float, required=False, default=0.05)
    parser.add_argument('-logscale', dest='logscale', help='scale the p-values according to log10', action='store_true',
                        required=False, default=False)
    parser.add_argument('-cmap', dest='cmap', help='output colormap file', required=False, default=None)

    args = parser.parse_args()
    shape_fdr(args.shapein, args.shapeout, args.method, args.mask, args.alpha, args.logscale, args.cmap)


def shape_fdr(shapein, shapeout, method, mask, alpha, logscale, cmap):

    s1 = Shape.readfile(shapein)
    s1.attributes = Stats_Multi_Comparisons.adjust(s1.attributes, method=method, alpha=alpha, maskfile=mask)

    cm = Colormap('pvalue', s1.attributes, log_transform=logscale)
    if logscale:
        s1.attributes = log_p_values(s1.attributes)

    Shape.writefile(shapeout, s1)

    if cmap is not None:
        cm.exportParaviewCmap(cmap + '.xml')
        cm.exportMayavi2LUT(cmap + '.map')


def log_p_values(pvalues):
    pvalues = pvalues[:]  # Make a copy because pvalues is passed by reference
    pminneg = -np.min(np.abs(pvalues[pvalues < 0]))
    pminpos = np.min(pvalues[pvalues > 0])

    if np.sum([pvalues >= 0]) > np.sum([pvalues <= 0]):
        pvalues[pvalues == 0] = pminpos
    else:
        pvalues[pvalues == 0] = pminneg

    pvalues = -np.sign(pvalues)*np.log10(np.abs(pvalues))
    return pvalues

if __name__ == '__main__':
    main()

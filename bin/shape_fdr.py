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


def main():
    parser = argparse.ArgumentParser(description='Adjust p-values by testing for multiple comparisons using fdr.\n')
    parser.add_argument('-i', dest='shapein', help='input surface', required=True)
    parser.add_argument('-o', dest='shapeout', help='output surface', required=True)
    parser.add_argument('-method', dest='method', help='correction method - holm, hochberg, bonferroni, BH, BY',
                        required=False, default="BH")

    args = parser.parse_args()
    shape_fdr(args.shapein, args.shapeout, args.method)


def shape_fdr(shapein, shapeout, method):

    s1 = Shape.readfile(shapein)
    s1.attributes = Stats_Multi_Comparisons.adjust(s1.attributes)
    Shape.writefile(shapeout, s1)

if __name__ == '__main__':
    main()

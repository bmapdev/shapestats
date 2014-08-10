#! /usr/local/epd/bin/python

"""Perform a two-sample independent t-test between shapes"""

__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2014, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "sjoshi@bmap.ucla.edu"
__credits__ = 'Inspired by the stats package rshape by Roger P. Woods'

import sys
import numpy as np
import argparse
import time
from shapeio.shape import Shape
from scipy.stats import ttest_ind
import shapestats.stats_mult_comp
import copy


def main():
    parser = argparse.ArgumentParser(description='This program performs a paired t-test between shapes.\n '
                                                 'The number of subjects should be same, and the number of shape '
                                                 'vertices for each subject should be same.')
    parser.add_argument('-sample1', dest='sample1', help='<txt file for sample 1>', required=True)
    parser.add_argument('-sample2', dest='sample2', help='<txt file for sample 1>', required=True)
    parser.add_argument('-o', dest='output_shape', help='<output file for shape>', required=True)
    parser.add_argument('-oFDR', dest='output_shape_fdr', help='<log file>', required=True)

    args = parser.parse_args()
    t = time.time()
    # do stuff
    ind_t_test_shape(args.sample1, args.sample2, args.output_shape, args.output_shape_fdr)
    elapsed = time.time() - t
    print elapsed


def ind_t_test_shape(sample1, sample2, output_shape, output_shape_fdr):


    s1, s1_average, attrib1_array = Shape.read_aggregated_attributes_from_surfaces(sample1)
    s2, s2_average, attrib2_array = Shape.read_aggregated_attributes_from_surfaces(sample2)

    if attrib1_array == [] or attrib1_array == []:
        sys.exit('Error in Reading one or more files...Now Exiting.\n')

    # If files are successfully read, then proceed with the t-test
    tstat_array, pvalue_array = ttest_ind(attrib1_array, attrib2_array)
    pvalue_array_with_sign = np.sign(tstat_array)*pvalue_array

    s1_average.attributes = pvalue_array_with_sign
    pvalue_array_adjusted = shapestats.stats_mult_comp.Stats_Multi_Comparisons.adjust(pvalue_array_with_sign, method='fdr_tsbh', alpha=0.05, maskfile=None)
    Shape.writefile(output_shape, s1_average)
    s1_average_with_adjusted = s1_average
    s1_average_with_adjusted.attributes = pvalue_array_adjusted
    Shape.writefile(output_shape_fdr, s1_average_with_adjusted)

    sys.stdout.write('Done.\n')
    return

if __name__ == '__main__':
    main()

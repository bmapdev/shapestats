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
from shapestats.stats_output import StatsOutput
from shapestats.stats_data import StatsData


def main():
    parser = argparse.ArgumentParser(description='This program performs a paired t-test between shapes.\n '
                                                 'The number of subjects should be same, and the number of shape '
                                                 'vertices for each subject should be same.')
    parser.add_argument('-sample1', dest='sample1', help='<txt file for sample 1>', required=True)
    parser.add_argument('-sample2', dest='sample2', help='<txt file for sample 1>', required=True)
    parser.add_argument('-odir', dest='odir', help='<output directory>', required=True)
    parser.add_argument('-prefix', dest='prefix', help='<output filename prefix>', required=False, default='stats_')
    parser.add_argument('-log_transform_stats', dest='log_transform_stats', help='log transform pvalues',
                        required=False, action='store_true', default=False)


    args = parser.parse_args()
    t = time.time()
    # do stuff
    ind_t_test_shape(args.sample1, args.sample2, args.odir, args.prefix, args.log_transform_stats)
    elapsed = time.time() - t
    print elapsed


def ind_t_test_shape(sample1, sample2, odir, prefix, log_transform_stats):

    statsdata = StatsData()
    statsdata.filext = Shape.determine_file_extension(sample1, contains_filelist=True)
    s1, s1_average, attrib1_array = Shape.read_aggregated_attributes_from_surfaces(sample1)
    s2, s2_average, attrib2_array = Shape.read_aggregated_attributes_from_surfaces(sample2)

    if attrib1_array == [] or attrib1_array == []:
        sys.exit('Error in Reading one or more files...Now Exiting.\n')

    # If files are successfully read, then proceed with the t-test
    tstat_array, pvalue_array = ttest_ind(attrib1_array, attrib2_array)
    pvalue_array_with_sign = np.sign(tstat_array)*pvalue_array

    statsout = StatsOutput()
    statsout.pvalues = pvalue_array_with_sign
    statsout.save(odir, prefix, statsdata=statsdata, shape_average=s1_average, save_vtp=True, log_transform=log_transform_stats)
    sys.stdout.write('Done.\n')
    return

if __name__ == '__main__':
    main()

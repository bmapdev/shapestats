#! /usr/local/epd/bin/python

"""Python interface to paired t-test"""

__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2013, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "s.joshi@ucla.edu"
__credits__ = 'Inspired by the stats package rshape by Roger P. Woods'

# import rpy2.robjects as robjects
import numpy as np
from stats_output import StatsOutput
# from rpy2.robjects import r
# r.library("data.table")
from sys import stdout
from scipy.stats import ttest_rel


def paired_ttest_block(model, sdata):
    # Group the pairs according to model.variable
    siz = sdata.phenotype_array.shape[1]
    statsout = StatsOutput(dim=siz)
    pvalues = np.ones(siz)
    tvalues = np.zeros(siz)
    groupids = list(set(sdata.demographic_data[model.variable]))
    if len(groupids) != 2:
        stdout.write('Error: For a paired t-test, the file ' + model.demographics + ' should contain only two groups.\n')
        return

    # Get the group indices of the data
    idx1 = sdata.demographic_data[model.variable][sdata.demographic_data[model.variable] == groupids[0]].index
    idx2 = sdata.demographic_data[model.variable][sdata.demographic_data[model.variable] == groupids[1]].index

    stdout.write('Computing paired ttests for blocks...')
    stdout.flush()
    for block_num, block_idx in enumerate(sdata.blocks_idx):
        stdout.write(str(block_num) + ', ')
        stdout.flush()
        attrib_array = sdata.phenotype_array[:, range(block_idx[0], block_idx[1])]

        tstat_array, pvalue_array = ttest_rel(attrib_array[idx1, :], attrib_array[idx2, :])
        pvalues[range(block_idx[0], block_idx[1])] = pvalue_array
        tvalues[range(block_idx[0], block_idx[1])] = tstat_array

    pvalues[np.isnan(pvalues)] = 1
    tvalues[np.isnan(tvalues)] = 1
    stdout.write('Done.\n')
    stdout.write('Saving output files...\n')
    stdout.flush()
    statsout.pvalues = np.sign(tvalues)*pvalues
    statsout.file_name_string = '_paired_test_by_' + model.variable
    return statsout

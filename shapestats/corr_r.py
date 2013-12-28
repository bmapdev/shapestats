#! /usr/local/epd/bin/python

"""R interface to correlation"""

__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2013, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "s.joshi@ucla.edu"
__credits__ = 'Inspired by the stats package rshape by Roger P. Woods'

import rpy2.robjects as robjects
import numpy as np
from stats_output import StatsOutput
from rpy2.robjects import r
r.library("data.table")


def corr_r_func():

    corr_r_funct_str = {'corr_r_func': '''<- function(x, y, methodstr)
                {
                    return(cor.test(x, y, method=methodstr))
                }
                '''}
    return corr_r_funct_str


def corr_shape_r(model, sdata):
    statsout = StatsOutput(dim=sdata.phenotype_array.shape[1])
    r_dataframe = sdata.get_r_pre_data_frame(model)
    robjects.r.assign('r_dataframe', r_dataframe)
    robjects.r(corr_r_func().keys()[0] + corr_r_func()[corr_r_func().keys()[0]])
    robjects.r('r_datatable <- data.table(r_dataframe)')

    varx = 'value'
    vary = model.variable_to_corr
    r_corr_cmd = 'result <- r_datatable[, as.list({0:s}({1:s}, {2:s}, \"{3:s}\")), by=variable]'.format(
        corr_r_func().keys()[0], varx, vary, "pearson")
    robjects.r(r_corr_cmd)

    result = robjects.globalenv['result']

    statsout.pvalues = np.array(result[list(result.names).index('p.value')])
    corr_coeff = np.array(result[list(result.names).index('estimate')])
    corr_coeff = corr_coeff[1:len(corr_coeff):2]
    statsout.pvalues = np.sign(corr_coeff)*statsout.pvalues[1:len(statsout.pvalues):2]
    return statsout

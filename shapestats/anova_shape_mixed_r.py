#! /usr/local/epd/bin/python

"""R interface to mixed anova_shape"""

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
r.library("lme4")


def anova_mixed_r_func():

    anova_mixed_r_funct_str = {'anova_mixed_r_func': '''<- function(formula_full, formula_null, unique_term)
                {
                  lm_full <- lmer(formula_full)
                  lm_null <- lmer(formula_null)

                  if (is.null(lm_full) || is.null(lm_null)){
                    return(1.0);
                  }
                  else{
                     model_comparison <- anova(lm_full, lm_null)
                     t_full <- fixef(lm_full)[[unique_term]];
                     pval<-model_comparison[["Pr(>Chisq)"]][2]
                     if (is.nan(pval)){
                       return (1.0)
                     }
                     else {
                       return (t_full/abs(t_full)*model_comparison[["Pr(>Chisq)"]][2]);
                     }
                   }
                }
                '''}
    return anova_mixed_r_funct_str


def anova_shape_mixed_r(model, sdata):

    statsout = StatsOutput(dim=sdata.phenotype_array.shape[1])
    r_dataframe = sdata.get_r_pre_data_frame(model)
    robjects.r.assign('r_dataframe', r_dataframe)
    robjects.r(anova_mixed_r_func().keys()[0] + anova_mixed_r_func()[anova_mixed_r_func().keys()[0]])
    robjects.r('r_datatable <- data.table(r_dataframe)')
    model_full = 'value' + ' ~ ' + model.fullmodel
    model_null = 'value' + ' ~ ' + model.nullmodel

    r_anova_cmd = 'result <- r_datatable[, as.list({0:s}({1:s}, {2:s}, \"{3:s}\")), by=variable]'.format(
        anova_mixed_r_func().keys()[0], model_full, model_null, model.unique)
    robjects.r(r_anova_cmd)
    result = robjects.globalenv['result']
    statsout.pvalues = list(result[1])
    print statsout.pvalues
    return statsout


# def anova_shape_mixed_r_nonoptimal(model, sdata):
#
#     pre_data_frame = sdata.create_r_pre_data_frame(model)
#     statsout = StatsOutput(dim=sdata.phenotype_array.shape[1])
#     for i in xrange(sdata.phenotype_array.shape[1]):
#         pre_data_frame['response'] = robjects.FloatVector(sdata.phenotype_array[:, i])
#         dataframe = robjects.DataFrame(pre_data_frame)
#
#         robj = robjects.r
#         fit_full = robj.lm(robjects.Formula('response' + ' ~ ' + model.fullmodel), data=dataframe)
#         fit_reduced = robj.lm(robjects.Formula('response' + ' ~ ' + model.nullmodel), data=dataframe)
#         model_diff = robjects.r.anova(fit_full, fit_reduced)
#
#         idx_unique = fit_full.rx2('coefficients').names.index(model.unique)
#         direction = np.sign(fit_full.rx2('coefficients')[idx_unique])
#         idx_pvalues = model_diff.names.index('Pr(>F)')
#         statsout.pvalues[i] = model_diff[idx_pvalues][1]
#         statsout.pvalues_signed[i] = direction*model_diff[idx_pvalues][1]
#         statsout.tvalues[i] = fit_full.rx2('coefficients')[idx_unique]
#     return statsout

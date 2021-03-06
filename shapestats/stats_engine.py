#! /usr/local/epd/bin/python

"""Class that encapsulates the underlying statistical engine that will execute statistical tests"""

__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2013, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "s.joshi@ucla.edu"
__credits__ = 'Inspired by the stats package rshape by Roger P. Woods'

from anova_shape_sm import anova_shape_sm
from anova_shape_r import anova_shape_r
from anova_shape_r import anova_shape_r_block
from anova_shape_r import anova_shape_r_nonoptimal
from anova_shape_mixed_r import anova_shape_mixed_r
from corr_r import corr_shape_r_block
from paired_ttest import paired_ttest_block


class StatsEngine(object):

    def __init__(self, model, stats_data, engine='sm'):
        self.engine = engine
        self.model = model
        self.stats_data = stats_data
        self.commands_statmodels = None
        self.commands_r = None
        self.define_stats_commands()

    def define_stats_commands(self):
        if self.engine == 'sm':
            self.commands = {'anova': anova_shape_sm,
                             'paired_ttest': paired_ttest_block,
                             }
        elif self.engine == 'R':
            self.commands = {'anova': anova_shape_r_block,
                             'anova_mixed': anova_shape_mixed_r,
                             'corr': corr_shape_r_block,
                             'paired_ttest': paired_ttest_block,
                             }

    def run(self):
        stats_out = self.commands[self.model.stat_test](self.model, self.stats_data)
        return stats_out

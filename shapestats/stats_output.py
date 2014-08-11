#! /usr/local/epd/bin/python

"""Output specification for statistical tests"""

__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2013, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "s.joshi@ucla.edu"
__credits__ = 'Inspired by the stats package rshape by Roger P. Woods'

import numpy as np
import os
from shapeio.shape import Shape
import sys
from stats_mult_comp import Stats_Multi_Comparisons
import colormaps


class StatsOutput(object):

    def __init__(self, dim=0):
        self.pvalues = np.zeros(dim)
        self.pvalues_signed = np.zeros(dim)
        self.pvalues_adjusted = np.zeros(dim)
        self.corrvalues = []  # Correlations
        self.tvalues = np.zeros(dim)
        self.file_name_string = ''

    def adjust_for_multi_comparisons(self):
            self.pvalues_adjusted = Stats_Multi_Comparisons.adjust(self.pvalues)

    @staticmethod
    def savefile(filename, s1, fdr=True):
        pass

    def save(self, outdir, outprefix, statsdata=None, atlas_filename=None, shape_average=None, save_vtp=False, log_transform=False):

        if statsdata is None:
            statsdata.filext = None

        self.adjust_for_multi_comparisons()
        if not atlas_filename and not shape_average:
            sys.stdout.write('Error: Either atlas shape file or a coordinate shape average has to be provided.\n')
            sys.stdout.write('Quitting without saving output.')
            return
        else:
            if atlas_filename and shape_average:  #When both are provided. Use the atlas
                shape_average = None

            if atlas_filename:
                if statsdata.filext is None:
                    statsdata.filext = '.vtp'
                s1 = Shape.readfile(atlas_filename)

            if shape_average:
                s1 = shape_average

            if statsdata.filext == '.vtp':
                save_vtp = False
            else:
                save_vtp = True

            if log_transform:
                log_pvalues = statsdata.log_transform_p_values(self.pvalues)
                s1.attributes = log_pvalues
                cmap_pvalues = colormaps.Colormap('pvalue', self.pvalues, log_transform=True)
            else:
                s1.attributes = self.pvalues
                cmap_pvalues = colormaps.Colormap('pvalue', self.pvalues, log_transform=False)

            if len(s1.attributes) != s1.coords.shape[0]:
                sys.stdout.write('Error: Dimension mismatch between the p-values and the number of vertices. '
                                 'Quitting without saving.\n')
            Shape.writefile(os.path.join(outdir, outprefix + '_pvalues' + self.file_name_string + statsdata.filext), s1)
            cmap_pvalues.exportParaviewCmap(os.path.join(outdir, outprefix + '_pvalues' + self.file_name_string + '.xml'))
            cmap_pvalues.exportMayavi2LUT(os.path.join(outdir, outprefix + '_pvalues' + self.file_name_string + '.cmap'))

            if save_vtp:
                Shape.writefile(os.path.join(outdir, outprefix + '_pvalues' + self.file_name_string + statsdata.filext + '.vtp'), s1)

            if len(self.pvalues_adjusted) > 0:

                if log_transform:
                    log_pvalues_adjusted = statsdata.log_transform_p_values(self.pvalues_adjusted)
                    s1.attributes = log_pvalues_adjusted
                    cmap_adjusted_pvalues = colormaps.Colormap('pvalue', self.pvalues_adjusted, log_transform=True)
                else:
                    s1.attributes = self.pvalues_adjusted
                    cmap_adjusted_pvalues = colormaps.Colormap('pvalue', self.pvalues_adjusted, log_transform=False)

                Shape.writefile(os.path.join(outdir, outprefix + '_pvalues_adjusted' + self.file_name_string + statsdata.filext), s1)
                # cmap_adjusted_pvalues = colormaps.Colormap('pvalue', s1.attributes, log_transform=True)
                cmap_adjusted_pvalues.exportParaviewCmap(os.path.join(outdir, outprefix + '_pvalues_adjusted' + self.file_name_string + '.xml'))
                cmap_adjusted_pvalues.exportMayavi2LUT(os.path.join(outdir, outprefix + '_pvalues_adjusted' + self.file_name_string + '.cmap'))

                if save_vtp:
                    Shape.writefile(os.path.join(outdir, outprefix + '_pvalues_adjusted' + self.file_name_string + statsdata.filext + '.vtp'), s1)
            if len(self.corrvalues) > 0:
                s1.attributes = self.corrvalues
                Shape.writefile(os.path.join(outdir, outprefix + '_corr' + self.file_name_string + statsdata.filext), s1)
                if save_vtp:
                    Shape.writefile(os.path.join(outdir, outprefix + '_corr' + self.file_name_string + statsdata.filext + '.vtp'), s1)
                self.corrvalues[np.abs(self.pvalues_adjusted) > 0.05] = 0
                s1.attributes = self.corrvalues
                Shape.writefile(os.path.join(outdir, outprefix + '_corr_adjusted' + self.file_name_string + statsdata.filext), s1)
                if save_vtp:
                    Shape.writefile(os.path.join(outdir, outprefix + '_corr_adjusted' + self.file_name_string + statsdata.filext + '.vtp'), s1)

                return


        # print s1.attributes

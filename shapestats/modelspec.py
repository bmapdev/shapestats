#! /usr/local/epd/bin/python

"""Model specification for statistical tests"""

__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2013, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "s.joshi@ucla.edu"
__credits__ = 'Inspired by the stats package rshape by Roger P. Woods'

import ConfigParser
import re
import sys
from stats_data import StatsData
import numpy as np


class ModelSpec(object):

    def __init__(self, modelfile):
        self.subjdir = ''
        self.subjectid = ''
        self.demographics = ''
        self.phenotype = ''
        self.phenotype_attribute_matrix_file = ''
        self.file = ''

        self.modeltype = ''
        self.fullmodel = ''
        self.nullmodel = ''
        self.stat_test = ''
        self.variables = ''
        self.variable = ''
        self.unique = ''
        self.factors = []
        self.atlas_shape = ''

        self.read_modelfile(modelfile)
        if self.stat_test.find('mixed') != -1:
            self.parse_mixed_model()
        else:
            self.parse_model()

    def read_modelfile(self, modelfile):
        config = ConfigParser.ConfigParser()
        config.read(modelfile)

        config.options(config.sections()[0])
        self.subjdir = config.get('subjectinfo', 'subjectdir')
        self.subjectid = config.get('subjectinfo', 'subjectid')
        self.file = config.get('subjectinfo', 'file')
        self.demographics = config.get('subjectinfo', 'demographics')
        self.phenotype = config.get('subjectinfo', 'phenotype')
        self.phenotype_attribute_matrix_file = config.get('subjectinfo', 'phenotype_attribute_matrix')
        self.atlas_shape = config.get('subjectinfo', 'atlas')


        self.modeltype = config.get('model', 'modeltype')
        self.variable = config.get('model', 'variable')
        self.fullmodel = config.get('model', 'fullmodel')
        self.nullmodel = config.get('model', 'nullmodel')
        # self.unique = config.get('model', 'unique')  # TODO: find this automaticallly in the future
        factorstring = config.get('model', 'factors')
        for i in re.split(' ', factorstring):
            self.factors.append(i.rstrip().lstrip())

        self.stat_test = config.get('model', 'test')

    def parse_mixed_model(self):
        # Parse fullmodel and nullmodel
        set_full = set()
        set_null = set()

        for i in re.findall("[a-zA-Z_]+", self.fullmodel):
            set_full.add(i.rstrip().lstrip())
        for i in re.findall("[a-zA-Z_]+", self.nullmodel):
            set_null.add(i.rstrip().lstrip())
        self.variables = set_full | set_null

    def parse_model(self):
        # Parse fullmodel and nullmodel
        set_full = set()
        set_null = set()
        for i in re.split('\+', self.fullmodel):
            set_full.add(i.rstrip().lstrip())
        for i in re.split('\+', self.nullmodel):
            set_null.add(i.rstrip().lstrip())
        self.variables = set_full | set_null
        self.unique = list(set_full - set_null)[0]  # TODO check: only one element should be present

    def validate_model(self):
        #TODO validate model
        pass


class ModelType(object):
    def __init__(self):
        pass

    def validate(self):
        pass

    model_types = ['modelcomparison', 'correlation']

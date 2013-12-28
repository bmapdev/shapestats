#! /usr/local/epd/bin/python

"""Model specification for statistical tests"""

__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2013, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "s.joshi@ucla.edu"
__credits__ = 'Inspired by the stats package rshape by Roger P. Woods'

import ConfigParser
import re


class ModelSpec(object):

    def __init__(self, modelfile):
        self.subjdir = ''
        self.subjectid = ''
        self.demographics = ''
        self.phenotype = ''
        self.phenotype_attribute_matrix_file = ''

        self.modeltype = ''
        self.fullmodel = ''
        self.nullmodel = ''
        self.stat_test = ''
        self.variables = ''
        self.unique = ''
        self.factors = []
        self.atlas_shape = ''
        self.read_modelfile(modelfile)
        self.parse_model()

    def read_modelfile(self, modelfile):
        config = ConfigParser.ConfigParser()
        config.read(modelfile)

        config.options(config.sections()[0])
        self.subjdir = config.get('subjectinfo', 'subjectdir')
        self.subjectid = config.get('subjectinfo', 'subjectid')
        self.demographics = config.get('subjectinfo', 'demographics')
        self.phenotype = config.get('subjectinfo', 'phenotype')
        self.phenotype_attribute_matrix_file = config.get('subjectinfo', 'phenotype_attribute_matrix')
        self.atlas_shape = config.get('subjectinfo', 'atlas_shape')


        self.modeltype = config.get('model', 'modeltype')
        self.fullmodel = config.get('model', 'fullmodel')
        self.nullmodel = config.get('model', 'nullmodel')
        factorstring = config.get('model', 'factors')
        for i in re.split(' ', factorstring):
            self.factors.append(i.rstrip().lstrip())

        self.stat_test = config.get('model', 'test')

    def parse_model(self):
        # Parse fullmodel and nullmodel
        set_full = set()
        set_null = set()
        for i in re.split('\+|', self.fullmodel):
            set_full.add(i.rstrip().lstrip())
        for i in re.split('\+', self.nullmodel):
            set_null.add(i.rstrip().lstrip())
        self.variables = set_full | set_null
        self.unique = list(set_full - set_null)[0]  # TODO check: only one element should be present

    def validate_model(self):
        #TODO validate model
        pass



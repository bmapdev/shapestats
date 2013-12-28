#! /usr/local/epd/bin/python

"""Data specification for statistical tests"""

__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2013, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "s.joshi@ucla.edu"
__credits__ = 'Inspired by the stats package rshape by Roger P. Woods'

from shapeio.shape import Shape
from glob import glob
import struct
import array
import os
import numpy as np
import rpy2.robjects as robjects
import pandas
import sys


class StatsData(object):

    def __init__(self, demographics_file, model):
        self.demographic_data = ''
        self.dataframe = None
        self.phenotype_files = []
        self.phenotype_array = None
        self.pre_data_frame = {}
        self.shape_average = None
        self.phenotype_dataframe = None
        self.filext = None
        self.read_demographics(demographics_file)

        if not model.phenotype_attribute_matrix_file and not model.phenotype:
            sys.stdout.write('Error: Phenotype is not set. Data frame will not be created.')
            return

        # Choose the phenotype_attribute_matrix binary data if phenotype is also set
        if model.phenotype_attribute_matrix_file and model.phenotype:
            self.read_subject_phenotype_attribute_matrix(model)
            self.create_data_frame(model)
            return

        if model.phenotype:
            self.read_subject_phenotype(model)

        self.create_data_frame(model)

    def read_demographics(self, demographics_file):
        filename, ext = os.path.splitext(demographics_file)
        if ext == '.csv':
            self.demographic_data = pandas.read_csv(demographics_file)
        elif ext == '.txt':
            self.demographic_data = pandas.read_table(demographics_file)

    def validate_data(self):
        #TODO routines for validating self.demographic_data
        pass

    def read_subject_phenotype(self, model):
        # Test the file and directory hierarchy
        if len(glob(os.path.join(model.subjdir, self.demographic_data[model.subjectid][0], '*' + model.phenotype + '*'))) > 0:
            for subjectid in self.demographic_data[model.subjectid]:
                self.phenotype_files.append(glob(os.path.join(model.subjdir, subjectid, '*' + model.phenotype + '*'))[0])
        elif len(glob(os.path.join(model.subjdir, self.demographic_data[model.subjectid][0] + '*' + model.phenotype + '*'))) > 0:
            for subjectid in self.demographic_data[model.subjectid]:
                self.phenotype_files.append(glob(os.path.join(model.subjdir, subjectid + '*' + model.phenotype + '*'))[0])
        else:
            sys.stdout.write('Error: Subject phenotype files not found. Tested two different directory hierarchies:\n')
            sys.stdout.write('Possibility 1: ' + os.path.join(model.subjdir, self.demographic_data[model.subjectid][0], '*' + model.phenotype + '*'))
            sys.stdout.write('Possibility 2: ' + os.path.join(model.subjdir, self.demographic_data[model.subjectid][0] + '*' + model.phenotype + '*'))
            return

        # Determine if the shape is a curve or a surface
        fname, ext = os.path.splitext(model.atlas_shape)
        self.filext = ext
        s1, s1_average, self.phenotype_array = Shape.read_aggregated_attributes_from_shapefilelist(self.phenotype_files)
        self.shape_average = s1_average

    def read_subject_phenotype_attribute_matrix(self, model):
        fid = open(model.phenotype_attribute_matrix_file, 'rb')
        rows = np.array(struct.unpack('i', fid.read(4)), dtype='uint32')[0]  #size(int32) = 4 bytes
        cols = np.array(struct.unpack('i', fid.read(4)), dtype='uint32')[0]  #size(int32) = 4 bytes
        arrayfloat = array.array('f')
        arrayfloat.fromfile(fid, rows*cols)
        self.phenotype_array = np.frombuffer(arrayfloat, dtype=np.float32, offset=0).reshape(cols, rows, order='F')
        fname, ext = os.path.splitext(model.atlas_shape)
        self.filext = ext

        fid.close()

    def create_data_frame(self, model):
        for i in model.variables:
            if i in model.factors:
                self.pre_data_frame[i] = self.demographic_data[i]
            else:
                # Use either one of Int, Str, or Float vectors
                if self.demographic_data[i][0].dtype.type in (np.int32, np.int64):
                    self.pre_data_frame[i] = self.demographic_data[i]
                elif self.demographic_data[i][0].dtype.type in (np.float32, np.float64): #TODO check this
                    self.pre_data_frame[i] = self.demographic_data[i]
        # Create the phenotype array data frame
        # Create the column names for vertices automatically
        colnames = []
        for i in xrange(self.phenotype_array.shape[1]):
            colnames.append('V'+str(i))

        temp_frame = pandas.DataFrame(self.phenotype_array)
        temp_frame.columns = colnames
        temp_frame[model.subjectid] = self.demographic_data[model.subjectid]

        tot_dataframe = pandas.merge(self.demographic_data, temp_frame)
        tot_dataframe = pandas.melt(tot_dataframe, id_vars=self.demographic_data.columns)
        self.phenotype_dataframe = tot_dataframe
        return

    def get_r_pre_data_frame(self, model):
        pre_data_frame = {}
        for i in self.phenotype_dataframe.columns:
            if i in model.factors:
                pre_data_frame[i] = robjects.FactorVector(self.phenotype_dataframe[i])
            else:
                # Use either one of Int, Str, or Float vectors
                if self.phenotype_dataframe[i].dtype.type in (np.int32, np.int64):
                    pre_data_frame[i] = robjects.IntVector(self.phenotype_dataframe[i])
                elif self.phenotype_dataframe[i].dtype.type in (np.float32, np.float64):
                    pre_data_frame[i] = robjects.FloatVector(self.phenotype_dataframe[i])
                else:
                    pre_data_frame[i] = robjects.FactorVector(self.phenotype_dataframe[i])

        return robjects.DataFrame(pre_data_frame)

    def create_r_pre_data_frame(self, model):
        pre_data_frame = {}
        for i in model.variables:
            if i in model.factors:
                pre_data_frame[i] = robjects.FactorVector(self.demographic_data[i])
            else:
                # Use either one of Int, Str, or Float vectors
                if self.demographic_data[i][0].dtype.type is np.int64:
                    pre_data_frame[i] = robjects.IntVector(self.demographic_data[i])
                elif self.demographic_data[i][0].dtype.type is np.float64:
                    pre_data_frame[i] = robjects.FloatVector(self.demographic_data[i])

        return pre_data_frame


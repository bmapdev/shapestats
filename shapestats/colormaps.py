#! /usr/local/epd/bin/python

"""Perform a two-sample independent t-test between shapes"""

__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2014, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "sjoshi@bmap.ucla.edu"
__credits__ = 'Inspired by the stats package rshape by Roger P. Woods'

import numpy as np


class Colormap:

    def __init__(self, value_type, attributes, log_transform=False):
        if value_type == 'pvalue':
            if log_transform:
                self.color_dict = self.create_bidirectional_log_pvalue_colormap(attributes)
            else:
                self.color_dict = self.create_bidirectional_pvalue_colormap(attributes)
        elif value_type == 'corr':
            self.color_dict = self.create_bidirect_corr_colormap(attributes)

        self.attrib_range, self.red_range, self.green_range, self.blue_range = self.make_color_bins()
        self.attributes = attributes

    def create_pfdr_colormap(self, attributes):
        """
        Colormap for fdr-adjusted p-values. Assumes adjusted values after significance lie in |p| < 0.05
        """
        # Make the dict object for red, green, and blue
        color_dict = {'red': [(-1.0, 0.7216, 0.7216),
                              (-0.05*1.0001, 0.7216, 0.7216),
                              (-0.05/1.0001, 0.0, 0.0),
                              (0-1e-9, 0.0, 0.0),
                              (0+1e-9, 1.0, 1.0),
                              (0.05/1.0001, 0.7216, 0.7216),
                              (0.05*1.0001, 0.7216, 0.7216),
                              (1.0, 1.0, 1.0)],
                      'green': [(-1.0, 0.7216, 0.7216),
                                (-0.05*1.0001, 0.7216, 0.7216),
                                (-0.05/1.0001, 0.0, 0.0),
                                (0-1e-9, 1.0, 1.0),
                                (0+1e-9, 1.0, 1.0),
                                (0.05/1.0001, 0.0, 0.0),
                                (0.05*1.0001, 0.7216, 0.7216),
                                (1.0, 0.7216, 0.7216)],
                      'blue': [(-1.0, 0.7216, 0.7216),
                               (-0.05*1.0001, 0.7216, 0.7216),
                               (-0.05/1.0001, 1.0, 1.0),
                               (0-1e-9, 1.0, 1.0),
                               (0+1e-9, 0.0, 0.0),
                               (0.05/1.0001, 0.0, 0.0),
                               (0.05*1.0001, 0.7216, 0.7216),
                               (1.0, 0.7216, 0.7216)],
                      }
        return color_dict

    def create_bidirectional_pvalue_colormap(self, attributes, pFDRneg=-0.05, pFDRpos=0.05):
        """
        Colormap for pvalues. Assumes pvalues lie in |p| <= 1
        """

        negmin = -np.min(np.abs(attributes[attributes < 0]))
        if np.abs(negmin) > 0.05:
            negmin = -0.001
        negmax = -np.max(np.abs(attributes[attributes < 0]))
        posmin = np.min(attributes[attributes > 0])
        if posmin > 0.05:
            posmin = 0.001

        posmax = np.max(attributes[attributes > 0])


        neg_range = np.linspace(-1, negmin, 5)
        pos_range = np.linspace(posmin, 1, 5)

        # Make the dict object for red, green, and blue
        color_dict = {'red': [(-1.0, 0.94, 0.94),
                              (-0.0501, 0.94, 0.94),
                              (-0.05, 0.0, 0.0),
                              (negmin, 0.0, 0.0),
                              (posmin, 1.0, 1.0),
                              (0.05, 1.0, 1.0),
                              (0.0501, 0.94, 0.94),
                              (1.0, 0.94, 0.94)],
                      'green': [(-1, 0.94, 0.94),
                                (-0.0501, 0.94, 0.94),
                                (-0.05, 0.0, 0.0),
                                (negmin, 0.794, 0.794),
                                (posmin, 1.0, 1.0),
                                (0.05, 0.0, 0.0),
                                (0.0501, 0.94, 0.94),
                                (1.0, 0.94, 0.94)],
                      'blue': [(-1, 0.94, 0.94),
                               (-0.0501, 0.94, 0.94),
                               (-0.05, 1.0, 1.0),
                               (negmin, 1.0, 1.0),
                               (posmin, 0.0, 0.0),
                               (0.05, 0.0, 0.0),
                               (0.0501, 0.94, 0.94),
                               (1.0, 0.94, 0.94)]
                      }
        return color_dict

    def create_bidirectional_log_pvalue_colormap_wrong(self, attributes, pFDRneg=-0.05, pFDRpos=0.05):
        """
        Colormap for pvalues. Assumes pvalues lie in |p| <= 1
        """

        negmin = -np.min(np.abs(attributes[attributes < 0]))
        posmin = np.min(attributes[attributes > 0])

        negminlog = np.log10(np.abs(negmin))
        posminlog = -np.log10(posmin)


        # Make the dict object for red, green, and blue
        color_dict = {'red': [(negminlog, 0.94, 0.94),
                              (-0.0501, 0.94, 0.94),
                              (-0.05, 0.0, 0.0),
                              (negmin, 0.0, 0.0),
                              (posmin, 1.0, 1.0),
                              (0.05, 1.0, 1.0),
                              (0.0501, 0.94, 0.94),
                              (1.0, 0.94, 0.94)],
                      'green': [(negminlog, 0.94, 0.94),
                                (-0.0501, 0.94, 0.94),
                                (-0.05, 0.0, 0.0),
                                (negmin, 0.794, 0.794),
                                (posmin, 1.0, 1.0),
                                (0.05, 0.0, 0.0),
                                (0.0501, 0.94, 0.94),
                                (1.0, 0.94, 0.94)],
                      'blue': [(negminlog, 0.94, 0.94),
                               (-0.0501, 0.94, 0.94),
                               (-0.05, 1.0, 1.0),
                               (negmin, 1.0, 1.0),
                               (posmin, 0.0, 0.0),
                               (0.05, 0.0, 0.0),
                               (0.0501, 0.94, 0.94),
                               (1.0, 0.94, 0.94)]
                      }
        return color_dict

    def create_bidirectional_log_pvalue_colormap(self, attributes, pFDRneg=-0.05, pFDRpos=0.05):

        negmin = -np.min(np.abs(attributes[attributes < 0]))
        if np.abs(negmin) > 0.05:
            negmin = -0.001

        negmax = -np.max(np.abs(attributes[attributes < 0]))
        posmin = np.min(attributes[attributes > 0])
        if posmin > 0.05:
            posmin = 0.001

        posmax = np.max(attributes[attributes > 0])

        pminneglog = -np.sign(negmin)*np.log10(np.abs(negmin))
        pminposlog = -np.sign(posmin)*np.log10(posmin)

        pex = np.max([np.abs(pminneglog), pminposlog])

        if not pFDRneg:
            pFDRneg = (-10**(-pex))*1.0001
        if not pFDRpos:
            pFDRpos = (10**(-pex))*1.0001

        pFDRneglog = -np.log10(np.abs(pFDRneg))
        pFDRposlog = -np.log10(np.abs(pFDRpos))

        # Make the dict object for red, green, and blue
        color_dict = {'red': [(-pex, 0.0, 0.0),
                              (-pFDRneglog, 0.0, 0.0),
                              (-pFDRneglog/1.0001, 1.0, 1.0),
                              (pFDRposlog/1.0001, 1.0, 1.0),
                              (pFDRposlog, 1.0, 1.0),
                              (pex, 1.0, 1.0)],
                      'green': [(-pex, 1.0, 1.0),
                                (-pFDRneglog, 0.0, 0.0),
                                (-pFDRneglog/1.0001, 1.0, 1.0),
                                (pFDRposlog/1.0001, 1.0, 1.0),
                                (pFDRposlog, 0.0, 0.0),
                                (pex, 1.0, 1.0)],
                      'blue': [(-pex, 1.0, 1.0),
                               (-pFDRneglog, 1.0, 1.0),
                               (-pFDRneglog/1.0001, 1.0, 1.0),
                               (pFDRposlog/1.0001, 1.0, 1.0),
                               (pFDRposlog, 0.0, 0.0),
                               (pex, 0.0, 0.0)],
                      }

        return color_dict

    def create_bidirect_corr_colormap(self, attributes):
        """
        Colormap for correlation. Assumes correlations lie in |r| <= 1
        """

        if np.any(attributes[attributes < 0]):
            negmin = -np.min(np.abs(attributes[attributes < 0]))
        else:
            negmin = 0
        if np.any(attributes[attributes < 0]):
            negmax = -np.max(np.abs(attributes[attributes < 0]))
        else:
            negmax = 0
        if np.any(attributes[attributes > 0]):
            posmin = np.min(attributes[attributes > 0])
        else:
            posmin = 0
        if np.any(attributes[attributes > 0]):
            posmax = np.max(attributes[attributes > 0])
        else:
            posmax = 0

        neg_range = np.linspace(negmax, negmin, 5)
        pos_range = np.linspace(posmin, posmax, 5)

        # Make the dict object for red, green, and blue
        color_dict = {'red': [(neg_range[0], 0.0, 0.0),
                              (neg_range[1], 0.0, 0.0),
                              (neg_range[2], 0.0, 0.0),
                              (neg_range[3], 0.254, 0.254),
                              (neg_range[4], 0.84, 0.84),
                              (pos_range[0], 0.84, 0.84),
                              (pos_range[1], 0.862, 0.862),
                              (pos_range[2], 0.917, 0.917),
                              (pos_range[3], 0.956, 0.956),
                              (pos_range[4], 1.0, 1.0)],
                      'green': [(neg_range[0], 1.0, 1.0),
                                (neg_range[1], 0.5, 0.5),
                                (neg_range[2], 0.0, 0.0),
                                (neg_range[3], 0.082, 0.082),
                                (neg_range[4], 0.84, 0.84),
                                (pos_range[0], 0.84, 0.84),
                                (pos_range[1], 0.0784, 0.0784),
                                (pos_range[2], 0.419, 0.419),
                                (pos_range[3], 0.6862, 0.6862),
                                (pos_range[4], 1.0, 1.0)],
                      'blue': [(neg_range[0], 1.0, 1.0),
                               (neg_range[1], 0.99, 0.99),
                               (neg_range[2], 0.98, 0.98),
                               (neg_range[3], 0.521, 0.521),
                               (neg_range[4], 0.84, 0.84),
                               (pos_range[0], 0.84, 0.84),
                               (pos_range[1], 0.1372, 0.1372),
                               (pos_range[2], 0.07, 0.07),
                               (pos_range[3], 0.0392, 0.0392),
                               (pos_range[4], 0.0, 0.0)]
                      }
        return color_dict

    def make_color_bins(self):
        red_color_list = self.color_dict['red']
        attribute_range = []
        red_range = []
        green_range = []
        blue_range = []

        for i in red_color_list:
            attribute_range.append(i[0])
            red_range.append(i[1])

        for i in self.color_dict['green']:
            green_range.append(i[1])

        for i in self.color_dict['blue']:
            blue_range.append(i[1])

        return np.array(attribute_range), np.array(red_range), np.array(green_range), np.array(blue_range)

    def get_rgb_from_attribute(self, value):

        value = float(value)
        # if abs(value) < 0.05:
        #     print "hi"
        idx1 = np.where((self.attrib_range <= value) == True)[0][-1]
        idx2 = np.where((self.attrib_range >= value) == True)[0][0]
        # Map the value from 0 to 1
        value = (value - self.attrib_range[idx1])/(self.attrib_range[idx2] - self.attrib_range[idx1] + 1e-8)
        red = (1.0 - value)*self.red_range[idx1] + value*self.red_range[idx2]
        green = (1.0 - value)*self.green_range[idx1] + value*self.green_range[idx2]
        blue = (1.0 - value)*self.blue_range[idx1] + value*self.blue_range[idx2]
        return (red, green, blue)

    def get_rgb_list_from_attribute_list(self, attribute_list):
        rgb_list = []
        for value in attribute_list:
            rgb_list.append(self.get_rgb_from_attribute(value))
        return rgb_list

    def scale(self, val, src, dst):
        """
        Scale the given value from the scale of src to the scale of dst.
        """
        return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

    def get_rgb_color_array(self, x=None):
        if x is None:
            x = self.attributes
        rgb_list = self.get_rgb_list_from_attribute_list(x)

        vColor = np.empty((3, len(x)))
        for idx, val in enumerate(rgb_list):
            vColor[:, idx] = [val[0], val[1], val[2]]
        vColor = np.ndarray.transpose(vColor)
        return vColor

    def exportParaviewCmap(self, filename):
        fid = open(filename, 'wt')
        fid.write('<ColorMap name="bi-direct" space="RGB">\n')

        for i in range(0, len(self.color_dict['red'])):
            xval, r, g, b = self.color_dict['red'][i][0], self.color_dict['red'][i][1], \
                            self.color_dict['green'][i][1], self.color_dict['blue'][i][1]
            fid.write('<Point x="{0:f}" o="1" r="{1:f}" g="{2:f}" b="{3:f}"/>\n'.format(float(xval), float(r), float(g), float(b)))

        fid.write('<NaN r="1" g="1" b="0"/>\n')
        fid.write('</ColorMap>\n')
        return None

    def exportMayavi2LUT(self, filename, lut_length=256):
        x = np.linspace(min(self.attrib_range), max(self.attrib_range), 256)
        LUT = self.get_rgb_color_array(x)
        fid = open(filename, 'wt')
        fid.write('LOOKUP_TABLE UnnamedTable 256\n')
        for i in range(0, len(LUT)):
            fid.write("{0:f} {1:f} {2:f} {3:f}\n".format(float(LUT[i, 0]), float(LUT[i, 1]), float(LUT[i, 2]), 1.0))

        fid.close()
        return None
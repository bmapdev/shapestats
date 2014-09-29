#! /usr/local/epd/bin/python

"""
Execute statistical modules in the package bst
"""

__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2013, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "s.joshi@ucla.edu"
__credits__ = 'Inspired by the stats package rshape by Roger P. Woods'

import argparse
import time
import logging
import os


def main():
    parser = argparse.ArgumentParser(description='Perform statistical analysis on Brainsuite processed data.\n')
    parser.add_argument('-modelspec', dest='modelspec', help='<txt file for model specification [ini]>', required=True)
    parser.add_argument('-outdir', dest='outdir', help='<output directory>', required=True)
    parser.add_argument('-outprefix', dest='outprefix', help='<output prefix>', required=False, default='hemi')
    parser.add_argument('-statsengine', dest='statsengine', help='<statistical engine [R/sm]>',
                        required=False, choices=['R', 'sm'], default='R')

    args = parser.parse_args()
    t = time.time()
    shapestats_model(args.modelspec, args.outdir, args.outprefix, args.statsengine)
    elapsed = time.time() - t
    os.sys.stdout.write("\nElapsed time " + str(elapsed) + " sec.")


def shapestats_model(modelspec, outdir, outprefix, opt_statsengine):
    from shapestats.modelspec import ModelSpec
    from shapestats.stats_data import StatsData
    from shapestats.stats_engine import StatsEngine

    if not os.path.exists(outdir):
        os.mkdir(outdir)
    logging.basicConfig(filename=os.path.join(outdir, 'shapestat.log'), level=logging.DEBUG,
                        format='%(levelname)s:%(message)s', filemode='w')
    logging.info('Reading model file ' + modelspec)
    model = ModelSpec(modelspec)
    logging.info('Done.')

    logging.info('Reading demographics file ' + model.demographics + ' and creating a data frame...')
    statsdata = StatsData(model.demographics, model)
    logging.info('Done.')

    logging.info('Computing ' + model.modeltype + ' with ' + model.stat_test + '...')
    statsengine = StatsEngine(model, statsdata, engine=opt_statsengine)
    statsoutput = statsengine.run()
    statsoutput.save(outdir, outprefix, statsdata, model.atlas_shape, statsdata.shape_average)
    logging.info('Done.')

if __name__ == '__main__':
    main()

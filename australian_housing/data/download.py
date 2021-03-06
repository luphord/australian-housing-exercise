# -*- coding: utf-8 -*-
import json
import logging
from pathlib import Path

import click
import requests

from .. import paths

DEFAULT_URL = 'http://stat.data.abs.gov.au/sdmx-json/data/ABS_BA_SA2_ASGS2016/' \
    + '1.9.1...0+1+102+1GSYD+10201.M/all?detail=Full&dimensionAtObservation=AllDimensions' \
    + '&startPeriod=2011-07&endPeriod=2017-07'

@click.command()
@click.option('--url',
    default=DEFAULT_URL,
    help='Download URL including query string')
def download(url):
    """Download data from Australia Bureau of Statistics.
       Output is saved in data/raw
    """
    logger = logging.getLogger(__name__)
    logger.info('download url is {}'.format(url))
    logger.info('downloading data...')
    json_data = requests.get(url).json()
    logger.info('json successfully downloaded')

    logger.info('saving data to {}...'.format(paths.manager.raw_data_file))
    with open(paths.manager.raw_data_file, 'w') as f:
        json.dump(json_data, f)
    logger.info('raw data saved')


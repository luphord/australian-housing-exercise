# -*- coding: utf-8 -*-
import json
import logging
from pathlib import Path

import click
import requests

@click.command()
@click.argument('url', type=click.Path())
def download(url):
    """Download data from Australia Bureau of Statistics.
       Output is saved in data/raw
    """
    logger = logging.getLogger(__name__)
    logger.info('downloading data')
    json_data = requests.get(url).json()

    project_dir = Path(__file__).resolve().parents[2]
    raw_data_dir = project_dir / 'data' / 'raw'
    raw_data_file = raw_data_dir / 'australian_housing.json'
    logger.info('saving data to {}'.format(raw_data_file))
    with open(raw_data_file) as f:
        json.dump(json_data, raw_data_file)
    logger.info('raw data saved')


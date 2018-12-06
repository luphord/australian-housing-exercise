# -*- coding: utf-8 -*-
import json
import logging
from pathlib import Path

import click
import pandas as pd

from .. import paths

def new_south_wales_index(df):
    return (df['Measure'] == 'Total number of dwelling units') \
        & (df['Sector of Ownership'] == 'Total Sectors') \
        & (df['Type of work'] == 'New') \
        & (df['Type of building'] == 'Houses') \
        & (df['Geography Level'] == 'States and Territories') \
        & (df['Region'] == 'New South Wales')

@click.command()
@click.option('--input_file', type=click.Path(exists=True), default=paths.manager.interim_data_file, help='Decoded dataframe containg all rows')
@click.option('--output_file', type=click.Path(), default=paths.manager.processed_data_file, help='Output file New South Wales timeseries')
def extract_timeseries(input_file, output_file):
    """Extract New South Wales timeseries from decoded dataframe.
       Output is saved in data/processed.
    """
    logger = logging.getLogger(__name__)
    logger.info('loading data')
    df = pd.read_csv(input_file)

    logger.info('indexing datafram')
    nsw = df[new_south_wales_index(df)]

    logger.info('saving data to {}'.format(output_file))
    nsw.to_csv(output_file)
    logger.info('New South Wales timeseries saved')

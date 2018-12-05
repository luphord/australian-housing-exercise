# -*- coding: utf-8 -*-
import json
import logging
from pathlib import Path

import click
import pandas as pd

project_dir = Path(__file__).resolve().parents[2]
interim_data_dir = project_dir / 'data' / 'interim'
interim_data_file = interim_data_dir / 'australian_housing_decoded.csv'
processed_data_dir = project_dir / 'data' / 'processed'
processed_data_file = processed_data_dir / 'new_south_wales_housing.csv'

@click.command()
@click.option('--input_file', type=click.Path(exists=True), default=interim_data_file, help='Decoded dataframe containg all rows')
@click.option('--output_file', type=click.Path(), default=processed_data_file, help='Output file New South Wales timeseries')
def extract_timeseries(input_file, output_file):
    """Extract New South Wales timeseries from decoded dataframe.
       Output is saved in data/processed.
    """
    logger = logging.getLogger(__name__)
    logger.info('loading data')
    df = pd.read_csv(interim_data_file)

    logger.info('indexing datafram')
    nsw = df[df['Region'] == 'New South Wales']

    logger.info('saving data to {}'.format(output_file))
    nsw.to_csv(output_file)
    logger.info('New South Wales timeseries saved')

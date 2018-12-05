# -*- coding: utf-8 -*-
import json
from datetime import datetime
import logging
from pathlib import Path

import click
import pandas as pd

project_dir = Path(__file__).resolve().parents[2]
raw_data_dir = project_dir / 'data' / 'raw'
raw_data_file = raw_data_dir / 'australian_housing.json'
interim_data_dir = project_dir / 'data' / 'interim'
interim_data_file = interim_data_dir / 'australian_housing_decoded.csv'

class AustralianHousingLoader:
    def __init__(self, sdmx_json):
        self.sdmx_json = sdmx_json

    def header(self):
        obs_codes = self.sdmx_json['structure']['dimensions']['observation']
        return [obs_code['name'] for obs_code in obs_codes] + ['Value']

    def decode(self):
        assert len(self.sdmx_json['dataSets']) == 1, 'Only SDMX json with a single dataset is supported, got {}'.format(len(self.sdmx_json['dataSets']))
        obs_codes = self.sdmx_json['structure']['dimensions']['observation']
        for idx, obs_code in enumerate(obs_codes):
            if 'keyPosition' in obs_code:
                assert(idx == int(obs_code['keyPosition'])), 'Observation code at index {} is {}'.format(idx, obs_code)
        for structured_key, values in self.sdmx_json['dataSets'][0]['observations'].items():
            key_parts = structured_key.split(':')
            assert len(key_parts) == len(obs_codes), 'Expected key of length {}, got {}'.format(len(obs_codes), len(key_parts))
            key_parts = [int(k) for k in key_parts]
            key_parts_decoded = []
            for idx, k in enumerate(key_parts):
                assert k < len(obs_codes[idx]['values']), 'Cannot decode index {}, because {}th value is requested, but there are only {} available'.format(idx, k, len(obs_code[idx]['values']))
                if obs_codes[idx]['id'] == 'TIME_PERIOD': # we immediately decode the string to a date
                    sdate = obs_codes[idx]['values'][k]['id']
                    key_parts_decoded.append(datetime.strptime(sdate, '%Y-%m'))
                else: # all non-date key parts are decoded using their code in dimensions
                    key_parts_decoded.append(obs_codes[idx]['values'][k]['name'])
            # we discard all but one of the values as they do not contain information (which we check for safety)
            assert values[1] == 0 and values[2] is None and values[3] == 0 and values[4] == 0, 'Got unexpected data in values {} at key {}'.format(values, structured_key)
            yield key_parts_decoded + values[:1]

    def to_dataframe(self):
        df = pd.DataFrame(self.decode(), columns=self.header())
        df.index = df['Time']
        return df

@click.command()
@click.option('--input_file', type=click.Path(exists=True), default=raw_data_file, help='Raw sdmx json input file')
@click.option('--output_file', type=click.Path(), default=interim_data_file, help='Output file for decoded data')
def extract_dataframe(input_file, output_file):
    """Decode raw json file and convert to dataframe.
       Output is saved in data/interim.
    """
    logger = logging.getLogger(__name__)
    logger.info('loading data')
    with open(input_file) as f:
        sdmx_json = json.load(f)

    logger.info('creating data frame')
    loader = AustralianHousingLoader(sdmx_json)
    df = loader.to_dataframe()

    logger.info('saving data to {}'.format(output_file))
    df.to_csv(output_file)
    logger.info('iterim data saved')

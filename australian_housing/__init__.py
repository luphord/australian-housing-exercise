import click

from .data.download import download
from .data.extract_dataframe import extract_dataframe
from .data.extract_timeseries import extract_timeseries

@click.group()
def main():
    pass

main.add_command(download)
main.add_command(extract_dataframe)
main.add_command(extract_timeseries)

import click

from .data.download import download
from .data.extract_dataframe import extract_dataframe

@click.group()
def main():
    pass

main.add_command(download)
main.add_command(extract_dataframe)

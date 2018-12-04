import click

from .data.download import download

@click.group()
def main():
    pass

main.add_command(download)

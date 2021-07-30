import click

from . import e2elink_cli
from .. import echo
from ...example.example import Example


def example_cmd():
    @e2elink_cli.command(help="Store example data in the current working directory")
    def example():
        echo("Getting example")
        examp = Example()
        examp.get()
        echo("Done", fg="green")

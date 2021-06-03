import click

from . import e2elink_cli
from .. import echo


def compare_cmd():

    @e2elink_cli.command(
        help="TODO"
    )
    def compare():
        echo("TODO")

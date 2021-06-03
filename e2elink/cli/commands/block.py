import click

from . import e2elink_cli
from .. import echo


def block_cmd():

    @e2elink_cli.command(
        help="TODO"
    )
    def block():
        echo("TODO")

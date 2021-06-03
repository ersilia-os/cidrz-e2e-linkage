import click

from . import e2elink_cli
from .. import echo


def preprocess_cmd():

    @e2elink_cli.command(
        help="TODO"
    )
    def preprocess():
        echo("TODO")

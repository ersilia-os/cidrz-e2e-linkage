import click

from . import e2elink_cli
from .. import echo


def score_cmd():
    @e2elink_cli.command(help="TODO")
    def score():
        echo("TODO")

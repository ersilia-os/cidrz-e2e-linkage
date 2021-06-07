import click

from . import e2elink_cli
from .. import echo

from ...steps.block.block import Blocker


def block_cmd():
    @e2elink_cli.command(help="Block")
    @click.option("--k", default=5, type=click.INT)
    def block(k):
        echo("Blocking")
        bl = Blocker().block(k)
        bl.save()
        echo("Done", fg="green")

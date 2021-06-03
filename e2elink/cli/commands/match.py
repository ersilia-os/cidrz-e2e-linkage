import click

from . import e2elink_cli
from .. import echo


def match_cmd():

    @e2elink_cli.command(
        help="Match schema"
    )
    def match():
        echo("Matching schema")
        
        echo("Done", fg="green")

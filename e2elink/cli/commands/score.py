import click

from . import e2elink_cli
from .. import echo
from ...steps.score.score import Scorer


def score_cmd():
    @e2elink_cli.command(help="Score comparisons")
    def score():
        echo("Scoring based on similarity metrics")
        sc = Scorer().score()
        sc.save()
        echo("Done", fg="green")

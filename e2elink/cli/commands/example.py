import click

from . import e2elink_cli
from .. import echo
from ...synthetic.sampler import SyntheticSampler


def example_cmd():

    @e2elink_cli.command(
        help="Sample datasets."
    )
    @click.option("--number", "-n", type=click.INT)
    def example(number):
        echo("Sampling data")
        samp = SyntheticSampler()
        samp.sample(number)
        echo("Done", fg="green")

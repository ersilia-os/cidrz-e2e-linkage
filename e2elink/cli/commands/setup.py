import click

from . import e2elink_cli
from .. import echo
from ...steps.setup.setup import PipelineSetup


def setup_cmd():

    @e2elink_cli.command(
        help="Setup pipeline. Creates an output directory."
    )
    @click.option("--src_file", type=click.STRING)
    @click.option("--trg_file", type=click.STRING)
    @click.option("--output_dir", default="output", type=click.STRING)
    def setup(src_file, trg_file, output_dir):
        echo("Setting up linkage task")
        ps = PipelineSetup(src_file, trg_file, output_dir)
        ps.setup()
        echo("Done", fg="green")

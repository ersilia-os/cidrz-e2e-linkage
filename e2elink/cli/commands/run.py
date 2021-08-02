import click

from . import e2elink_cli
from .. import echo
from ...steps.run import RunAll


def run_cmd():
    @e2elink_cli.command(help="Run full pipeline")
    @click.option("--src_file", type=click.STRING)
    @click.option("--trg_file", type=click.STRING)
    @click.option("--truth_file", default=None, type=click.STRING)
    @click.option("--output_dir", default="output", type=click.STRING)
    def run(src_file, trg_file, truth_file, output_dir):
        echo("Running pipeline")
        run = RunAll(src_file, trg_file, truth_file, output_dir)
        run.run()

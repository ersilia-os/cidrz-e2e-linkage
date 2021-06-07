from . import e2elink_cli
from .. import echo

from ...steps.compare.compare import Compare


def compare_cmd():
    @e2elink_cli.command(help="Compare")
    def compare():
        echo("Compare")
        comp = Compare().compare()
        comp.save()
        echo("Done", fg="green")

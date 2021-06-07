from . import e2elink_cli
from .. import echo

from ...steps.schema.schema import SchemaMatcher


def schema_cmd():
    @e2elink_cli.command(help="Match schema")
    def schema():
        echo("Matching schema")
        schema = SchemaMatcher().match()
        schema.save()
        echo("Done", fg="green")

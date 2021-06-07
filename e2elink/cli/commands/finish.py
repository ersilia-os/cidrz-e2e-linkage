from . import e2elink_cli
from .. import echo
from ...steps.finish.finish import Finisher


def finish_cmd():
    @e2elink_cli.command(help="Finish pipeline and prepare results")
    def finish():
        echo("Preparing output results")
        fin = Finisher().finish()
        fin.save()
        echo("Done", fg="green")

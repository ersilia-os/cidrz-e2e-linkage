from . import e2elink_cli
from .. import echo

from ...steps.preprocess.preprocess import Preprocessor


def preprocess_cmd():
    @e2elink_cli.command(help="Preprocess data")
    def preprocess():
        echo("Preprocessing")
        prep = Preprocessor().clean()
        prep.save()
        echo("Done", fg="green")

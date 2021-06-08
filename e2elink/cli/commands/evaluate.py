from . import e2elink_cli
from .. import echo
from ...steps.evaluate.evaluate import Evaluator


def evaluate_cmd():
    @e2elink_cli.command(help="Evaluate results")
    def evaluate():
        echo("Evaluating results")
        eval = Evaluator().evaluate()
        eval.save()
        echo("Done", fg="green")

from . import e2elink_cli
from .. import echo
from ...steps.preprocessing.e2e_pprocessor import  PreprocessPipelineHandler


from ...steps.preprocess.preprocess import Preprocessor


def preprocess_cmd(pipeline_setup=None, schema_match=None):


    @e2elink_cli.command(help="Preprocess data")
    def preprocess():
        """
    input: reference columns
            src file
            target file
            output files
        """
        echo("Preprocessing")

        prep = PreprocessPipelineHandler(pipeline_setup, schema_match)
        prep.clean()
        prep.save()

        echo("Done", fg="green")

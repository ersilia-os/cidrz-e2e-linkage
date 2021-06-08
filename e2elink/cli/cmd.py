class Command(object):
    def __init__(self):
        pass

    def example(self):
        from .commands.example import example_cmd

        example_cmd()

    def setup(self):
        from .commands.setup import setup_cmd

        setup_cmd()

    def schema(self):
        from .commands.schema import schema_cmd

        schema_cmd()

    def preprocess(self):
        from .commands.preprocess import preprocess_cmd

        preprocess_cmd()

    def block(self):
        from .commands.block import block_cmd

        block_cmd()

    def compare(self):
        from .commands.compare import compare_cmd

        compare_cmd()

    def score(self):
        from .commands.score import score_cmd

        score_cmd()

    def evaluate(self):
        from .commands.evaluate import evaluate_cmd

        evaluate_cmd()

    def finish(self):
        from .commands.finish import finish_cmd

        finish_cmd()

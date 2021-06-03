
from .cmd import Command
from .commands import e2elink_cli

def create_cli():

    cmd = Command()

    cmd.example()
    
    cmd.setup()
    cmd.match()
    cmd.preprocess()
    cmd.block()
    cmd.compare()
    cmd.score()

    return e2elink_cli

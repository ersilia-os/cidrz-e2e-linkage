import os
from pathlib import Path

E2ELINK_DIR = os.path.join(str(Path.home()), "e2elink")
if not os.path.exists(E2ELINK_DIR):
    os.makedirs(E2ELINK_DIR)

LOGGING_FILE = "console.log"

import os
from pathlib import Path

# Paths

E2ELINK_DIR = os.path.join(str(Path.home()), "e2elink")
if not os.path.exists(E2ELINK_DIR):
    os.makedirs(E2ELINK_DIR)

MODELS_PATH = os.path.join(E2ELINK_DIR, "models")
if not os.path.exists(MODELS_PATH):
    os.makedirs(MODELS_PATH)

# File names

LOGGING_FILE = "console.log"

import sys
from pathlib import Path

# add base project path to PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
print(BASE_DIR)
"""Print the claims library hash (skills stamp it into output headers)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "verify"))
from check_ids import library_hash
print(library_hash())

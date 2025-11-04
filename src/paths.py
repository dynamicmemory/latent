from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


def get_data_path(fname: str) -> Path:
    """ 
    Links the given file name to the correct directory for access to the dbs
    """
    return DATA_DIR / fname

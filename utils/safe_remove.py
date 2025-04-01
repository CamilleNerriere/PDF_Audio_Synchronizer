import os
from utils.logger import logger

def safe_remove(path : str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        logger.warning(f"[WARN] Unable to delete path : {e}")
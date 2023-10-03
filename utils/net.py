import requests
from pathlib import Path
import logging
import os
import hashlib


# TODO: implement that caches that are too old are not used
def cached_get(url, base_path=Path("/tmp/cache/")) -> str:
    """
    Returns a response_text
    """
    LOGGING = logging.getLogger("Net")

    LOGGING.debug(f"Cached get to url: {url}")

    cache_folder_path = Path(base_path)
    cache_file = f"{hashlib.md5(str(url).encode('utf-8')).hexdigest()}.txt"
    cache_path = cache_folder_path / cache_file
    if os.path.isdir(cache_folder_path) and os.path.exists(cache_path):
        LOGGING.debug(f"Getting cached url {url} for {str(cache_path)}")
        with open(cache_path) as f:
            response_text = f.read()
    else:
        response = requests.get(url)
        response_text = response.text
        cache_folder_path.mkdir(parents=True, exist_ok=True)
        LOGGING.debug(f"Caching url {url} to {str(cache_path)}")
        with open(cache_path, "w") as f:
            f.write(response_text)

    return response_text

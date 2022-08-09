import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from subprocess import getoutput

from github import Github

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

api_key = os.getenv("api_key", None)
current_date = datetime.today().strftime("%Y-%m-%d")

try:
    path = list(
        (Path(os.path.dirname(os.path.abspath(__file__))) / "../../dist").glob(
            "hascal*"
        )
    )[0]
except IndexError:
    logging.error("No built binary found")
    sys.exit(1)

repo_name = os.getenv("name", None)
release_name = os.getenv("release_name", None)

if release_name is None:
    release_name = getoutput("git describe --tags --always")

logging.info("Starting at %s", current_date)

if not (repo_name and api_key and release_name):
    logging.error(
        "'repo_name'/'api_key'/'release_name' not found in your envs."
        "please add this and run again"
    )
    sys.exit(1)


gh = Github(api_key)
repo = gh.get_repo(f"hascal/{repo_name}")

release = repo.get_release(release_name)

logging.info("statrting Upload build file to release")

release.upload_asset(path=path)
logging.info("upload is done")

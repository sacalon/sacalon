import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from platform import system
from subprocess import getoutput

from github import Github

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

api_key = os.getenv("api_key", None)
release_name = os.getenv("release_name", None)

if not (api_key and release_name):
    logging.error(
        "'api_key'/'release_name' not found in your envs."
        f"please add this and run again, your envs are: {api_key} and {release_name}"
    )
    sys.exit(1)


# build
logging.info(msg="Building...")
if system() == "Windows":
    os.system("make windows")
else:
    os.system("make build")
logging.info(msg="Build complete")

try:
    path = list(
        (Path(os.path.dirname(os.path.abspath(__file__))) / "../../dist").glob(
            "sacalon*"
        )
    )[0]
except IndexError:
    logging.error("No built binary found")
    sys.exit(1)

if system().lower().startswith("nt"):
    name = "windows"
elif system().lower().startswith("linux"):
    name = "linux"
elif system().lower().startswith("darwin"):
    name = "macos"
else:
    name = system().lower()

path = (
    Path(os.path.dirname(os.path.abspath(__file__)))
    / "../../"
    / path.rename(f"sacalon-{name}-{release_name}")
)

gh = Github(api_key)
repo = gh.get_repo("sacalon-lang/sacalon")

release = repo.get_release(release_name)
logging.info("statrting Upload build file to release")
release.upload_asset(path=str(os.path.normpath(path)))
logging.info("upload is done")

from .sa_error import SacalonError
from subprocess import DEVNULL, STDOUT, check_call

def check_if_git_installed():
    try:
        check_call(["git", "--version"], stdout=DEVNULL, stderr=STDOUT)
    except:
        SacalonError("Git is not installed, please install it")

def check_if_git_repo_exist(url):
    if url.startswith("https://") or url.startswith("http://"):
        SacalonError(f"{url} is not a valid git repository url")

    try:
        check_call(["git", "ls-remote", "https://" + url + ".git"], stdout=DEVNULL, stderr=STDOUT)
    except:
        try : 
            check_call(["git", "ls-remote", "https://" + url + ".git"], stdout=DEVNULL, stderr=STDOUT)
        except:
            SacalonError(f"Module '{url}' is not available or is a private git repository")

def clone_repo(url, path):
    try:
        check_call(["git", "clone", "https://" + url + ".git", path], stdout=DEVNULL, stderr=STDOUT)
    except:
        try :
            check_call(["git", "clone", "https://" + url + ".git", path], stdout=DEVNULL, stderr=STDOUT)
        except:
            SacalonError(f"Cannot clone module '{url}'")

def update_repo(path):
    try:
        check_call(["git", "pull"], cwd=path, stdout=DEVNULL, stderr=STDOUT)
    except:
        SacalonError(f"Cannot update module '{path}'")
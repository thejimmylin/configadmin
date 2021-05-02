import sys
from pathlib import Path

from invoke import task

from configadmins import JsonConfigAdmin

REPO_ROOT = Path(__file__).parent
PYTHON_PATH = Path(sys.executable)
PYTHON_PATH_RELATIVE = Path(sys.executable).relative_to(REPO_ROOT)

VSCODE_SETTINGS_PYTHON = {
    "python.pythonPath": str(PYTHON_PATH_RELATIVE),
    "python.linting.enabled": True,
    "python.linting.pylintEnabled": False,
    "python.linting.flake8Enabled": True,
    "python.linting.flake8Args": ["--max-line-length=88"],
    "python.formatting.provider": "black",
}

VSCODE_SETTINGS_VUE = {
    "prettier.tabWidth": 4,
    "prettier.printWidth": 160,
    "vetur.format.options.tabSize": 4,
    "vetur.format.defaultFormatterOptions": {"prettier": {"printWidth": 160}},
}

SECRETS = {
    "GMAIL_EMAIL_HOST_PASSWORD": "",
}


@task
def setdefaultconfig(c):
    JsonConfigAdmin(
        path=REPO_ROOT / ".vscode" / "settings.json", options=VSCODE_SETTINGS_PYTHON
    ).live().setdefault()
    JsonConfigAdmin(
        path=REPO_ROOT / ".vscode" / "settings.json", options=VSCODE_SETTINGS_VUE
    ).live().setdefault()
    JsonConfigAdmin(
        path=REPO_ROOT / "secrets.json", options=SECRETS
    ).live().setdefault()


@task
def updateconfig(c):
    JsonConfigAdmin(
        path=REPO_ROOT / ".vscode" / "settings.json", options=VSCODE_SETTINGS_PYTHON
    ).live().update()
    JsonConfigAdmin(
        path=REPO_ROOT / ".vscode" / "settings.json", options=VSCODE_SETTINGS_VUE
    ).live().update()
    JsonConfigAdmin(path=REPO_ROOT / "secrets.json", options=SECRETS).live().update()

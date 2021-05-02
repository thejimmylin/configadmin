# configadmin
 Admin your config easily

# Overview

configadmins.py
```python
import json
from pathlib import Path


class JsonConfigAdmin:
    def __init__(self, path=Path(), options={}, encoding="utf-8", empty="{}"):
        self.path = path
        self.options = options
        self.encoding = encoding
        self.empty = empty

    def live(self, parents=True, exist_ok=True):
        self.path.parent.mkdir(parents=parents, exist_ok=exist_ok)
        self.path.touch(exist_ok=exist_ok)
        return self

    def is_proceeded(self, yes="y", no="n"):
        while True:
            print(f"Proceed ({yes}/{no})?", end=" ")
            response = input()
            if response == yes:
                return True
            if response == no:
                return False
            print(
                f"Your response ({response}) was not one of the expected responses: "
                f"{yes}, {no}"
            )
        return self

    def update(self, indent=4, encoding=None):
        warning = (
            f'Would you want to update "{self.path}"?\n'
            "The options below would be used:\n"
            f"{json.dumps(self.options, indent=indent)}"
        )
        print(warning)
        proceeded = self.is_proceeded()
        if not proceeded:
            print("Operation was interrupted.")
            return
        content = self.path.read_text(encoding=encoding) or self.empty
        options = json.loads(content)
        new_options = self.options
        options.update(new_options)
        new_content = json.dumps(options, indent=indent)
        self.path.write_text(new_content, encoding=encoding)
        print(f'Successfully updated "{self.path}".\n')
        return self

    def setdefault(self, indent=4, encoding=None):
        warning = (
            f'Would you want to "setdefault" on "{self.path}"?\n'
            "The options below would be used:\n"
            f"{json.dumps(self.options, indent=indent)}"
        )
        print(warning)
        proceeded = self.is_proceeded()
        if not proceeded:
            print("Operation was interrupted.")
            return
        content = self.path.read_text(encoding=encoding) or self.empty
        options = json.loads(content)
        new_options = self.options
        for key, value in new_options.items():
            options.setdefault(key, value)
        new_content = json.dumps(options, indent=indent)
        self.path.write_text(new_content, encoding=encoding)
        print(f'Successfully updated "{self.path}".\n')
        return self

```

# Usage 🎃

tasks.py
```python
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

```

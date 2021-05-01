# configadmin
 Admin your config easily

# Usage

```python
import sys
from pathlib import Path

from invoke import task

from configadmin import JsonConfig

REPO_ROOT = Path(__file__).parent
PYTHON_PATH = Path(sys.executable)
PYTHON_PATH_RELATIVE = Path(sys.executable).relative_to(REPO_ROOT)

VSCODE_SETTINGS_PYTHON = {
    'python.pythonPath': str(PYTHON_PATH_RELATIVE),
    'python.linting.enabled': True,
    'python.linting.pylintEnabled': False,
    'python.linting.flake8Enabled': True,
    'python.linting.flake8Args': ['--max-line-length=160'],
    'python.formatting.provider': 'autopep8',
    'python.formatting.autopep8Args': ['--max-line-length=160'],
}

VSCODE_SETTINGS_VUE = {
    'prettier.tabWidth': 4,
    'prettier.printWidth': 160,
    'vetur.format.options.tabSize': 4,
    'vetur.format.defaultFormatterOptions': {
        'prettier': {
            'printWidth': 160
        }
    }
}

SECRETS = {
    'GMAIL_EMAIL_HOST_PASSWORD': '',
}


@task
def setdefaultconfig(c):
    python = JsonConfig(path=REPO_ROOT / '.vscode' / 'settings.json', options=VSCODE_SETTINGS_PYTHON)
    python.live()
    python.setdefault()
    vue = JsonConfig(path=REPO_ROOT / '.vscode' / 'settings.json', options=VSCODE_SETTINGS_PYTHON)
    vue.live()
    vue.setdefault()
    secrets = JsonConfig(path=REPO_ROOT / 'secrets.json', options=SECRETS)
    secrets.live()
    secrets.setdefault()


@task
def updateconfig(c):
    python = JsonConfig(path=REPO_ROOT / '.vscode' / 'settings.json', options=VSCODE_SETTINGS_PYTHON)
    python.live()
    python.update()
    vue = JsonConfig(path=REPO_ROOT / '.vscode' / 'settings.json', options=VSCODE_SETTINGS_PYTHON)
    vue.live()
    vue.update()
    secrets = JsonConfig(path=REPO_ROOT / 'secrets.json', options=SECRETS)
    secrets.live()
    secrets.update()

```

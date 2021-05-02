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

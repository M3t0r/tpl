import os
from pathlib import Path
from subprocess import run, PIPE, CompletedProcess
from collections import defaultdict
import json


import pytest
import yaml


EXECUTION_TIMEOUT = 2  # seconds


class CLI:
    """Helper class to ease testing of CLI commands"""
    def __init__(self, executable_list, tmpdir, print_debug_output=True):
        self._executable = executable_list
        self.tmpdir = tmpdir
        self._tmpfile_auto_increment = defaultdict(int)
        # print stdout/err and exit code so that in case of errors we can see
        # what happened
        self._print_debug_output = print_debug_output

    def __call__(self, *args, stdin="", env={}, encoding="UTF-8") -> CompletedProcess:
        # patch PATH into env if not already set
        env.setdefault("PATH", os.environ["PATH"])
        result = run(
            ["tpl", *[str(arg) for arg in args]],
            timeout=EXECUTION_TIMEOUT,
            stdout=PIPE,
            stderr=PIPE,
            input=str(stdin).encode(encoding),
            env=env,
            cwd=str(self.tmpdir)
        )

        # Python 3.5 doesn't support the `encoding` argument to `run()`,
        # so we have to manually decode the byte strings
        result.stdout = result.stdout.decode(encoding)
        result.stderr = result.stderr.decode(encoding)

        if self._print_debug_output:
            self.print_debug_info_for_call(result)
        return result

    def _print_stream_output(self, call_result: CompletedProcess, stream_name: str):
        stream = getattr(call_result, stream_name.lower())
        name = stream_name.upper()

        print(name + ":", end="")
        if len(stream) == 0:
            print(" (stream is empty)")
        elif stream == "\n":
            print(" (stream is empty, containts only one newline)")
        elif stream[-1] != "\n":
            print(" (does not end in newline)")
        else:
            print()

        print("-" * 24)

        print(stream, end="")

        # if it doesn't end in a newline add one so the seperation doesn't start
        # directly after the output
        if len(stream) > 0 and stream[-1] != "\n":
            print()

        print("=" * 24)

    def print_debug_info_for_call(self, call_result: CompletedProcess):
            print("Command:", call_result.args)
            print("Return code:", call_result.returncode)

            self._print_stream_output(call_result, "stdout")
            self._print_stream_output(call_result, "stderr")

            print("Folder hierarchy:")
            print(self.folder_tree())

    def folder_tree(self, path=None):
        if path is None:
            path = self.tmpdir
        path = Path(str(path))
        return "./\n" + "\n".join(self._folder_structure_recursive(path))

    def _folder_structure_recursive(self, path: Path):
        for item in path.iterdir():
            yield "|-- " + item.name
            if item.is_dir():
                for line in self._folder_structure_recursive(item):
                    yield "|   " + line

    def _normalize_filename(self, name):
        allowed_chars = (
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "01234567890"
            "-_."
        )
        return "".join([c for c in str(name) if c in allowed_chars][:32])

    def unique_file(self, name="") -> Path:
        """Generate a unique filename that can be used in the tmpdir"""
        normalized = self._normalize_filename(name)

        index = str(self._tmpfile_auto_increment[normalized])
        self._tmpfile_auto_increment[normalized] += 1

        filename = normalized + "-" + index
        if len(normalized) == 0:
            filename = index

        return Path(str(self.tmpdir), filename)

    def path_for_content(self, file_content, encoding="UTF-8", name="") -> Path:
        if name == "":
            name = file_content  # use the first few characters to form a name
        file_path = self.unique_file(name)
        with file_path.open("wb") as file:
            file.write(str(file_content).encode(encoding))
        return file_path

    def path_for_json(self, content: dict, encoding="UTF-8", name="") -> Path:
        if name == "":
            name = "json-data"
        return self.path_for_content(json.dumps(content), encoding, name)

    def path_for_yaml(self, content: dict, encoding="UTF-8", name="") -> Path:
        if name == "":
            name = "yaml-data"
        return self.path_for_content(
            yaml.dump(content, default_flow_style=False),
            encoding,
            name
        )


@pytest.fixture
def cli(tmpdir):
    yield CLI("tpl", tmpdir)

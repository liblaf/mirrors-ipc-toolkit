import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, override

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    _tmpdir: Path

    @override
    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        tmpdir: Path = Path(tempfile.mkdtemp())
        self._tmpdir = tmpdir
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pybind11_stubgen",
                f"--output-dir={tmpdir}",
                "--root-suffix=-stubs",
                "--ignore-all-errors",
                "--exit-code",
                "ipctk",
            ],
            check=True,
        )
        build_data["force_include"][os.fspath(tmpdir / "ipctk-stubs")] = "ipctk-stubs"

    @override
    def finalize(
        self, version: str, build_data: dict[str, Any], artifact_path: str
    ) -> None:
        shutil.rmtree(self._tmpdir, ignore_errors=True)

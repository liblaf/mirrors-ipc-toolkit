#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "githubkit>=0.15.5",
# ]
# ///
import argparse
import asyncio
import json
from pathlib import Path
from typing import Required, Self, TypedDict

from githubkit import ActionAuthStrategy, GitHub
from githubkit.versions.latest.models import Release


class Package(TypedDict, total=False):
    filename: Required[str]
    hash: str
    requires_python: str
    uploaded_by: str
    upload_timestamp: int


class Args(argparse.Namespace):
    output: Path

    @classmethod
    def parse_args(cls) -> Self:
        parser: argparse.ArgumentParser = argparse.ArgumentParser()
        parser.add_argument("-o", "--output", default=Path("packages.jsonl"), type=Path)
        return parser.parse_args(namespace=cls())


async def main() -> None:
    args: Args = Args.parse_args()
    gh: GitHub = GitHub(ActionAuthStrategy())
    release: Release = (
        await gh.rest.repos.async_get_release_by_tag(
            owner="liblaf", repo="mirrors-ipc-toolkit", tag="latest"
        )
    ).parsed_data
    package_list: list[Package] = []
    for asset in release.assets:
        package: Package = {
            "filename": asset.name,
            "requires_python": ">=3.6",
            "upload_timestamp": int(asset.created_at.timestamp()),
        }
        if asset.digest:
            package["hash"] = asset.digest.replace(":", "=")
        if asset.uploader:
            package["uploaded_by"] = asset.uploader.login
        package_list.append(package)
    with args.output.open("w") as fp:
        for package in package_list:
            json.dump(package, fp)
            fp.write("\n")


if __name__ == "__main__":
    asyncio.run(main())

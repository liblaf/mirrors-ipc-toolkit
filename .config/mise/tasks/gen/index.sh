#!/bin/bash
# [MISE] depends=["gen:packages"]
set -o errexit
set -o nounset
set -o pipefail

uvx dumb-pypi \
  --package-list-json 'packages.jsonl' \
  --output-dir 'gh-pages' \
  --packages-url 'https://github.com/liblaf/mirrors-ipc-toolkit/releases/download/latest/'

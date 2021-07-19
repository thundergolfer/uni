#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"

main() {
  pushd "$REPO_ROOT"
  bazel build //books/fp_in_scala/src/main/scala/fpinscala/gettingstarted:repl
  ./bazel-bin/books/fp_in_scala/src/main/scala/fpinscala/gettingstarted/repl
  popd "$REPO_ROOT"
}

main "$@"

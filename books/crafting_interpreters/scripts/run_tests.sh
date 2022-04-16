#! /usr/bin/env nix-shell
#! nix-shell -i bash ./shell.nix
# shellcheck shell=bash

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"

build_interpreters() {
  bazel build //books/crafting_interpreters/jlox/lox:Lox_deploy.jar
}

create_temp_jlox_exe_script() {
  exe="${1}"

  tmpfile=$(mktemp /tmp/jlox.XXXXXX)
  {
    echo "#!/usr/bin/env bash"
    echo "set -euo pipefail"
    echo ""
    echo "java -jar ${exe} \$@"
  } >> $tmpfile

  echo $tmpfile
}

# I tried to integrate munificent/craftinginterpreters's Dartlang
# test runner into this repo's Bazel workspace, but I don't know Dartlang
# at all and it was too annoying.
#
# So this script exists to connect my Bazel-built Lox interpreters to
# the github.com/munificent/craftinginterpreters test runner.
main() {
  pushd "$REPO_ROOT"

  craftinginterpreters_git_location="git@github.com:munificent/craftinginterpreters"
  craftinginterpreters_repo_location="/Users/jonathon/Code/thundergolfer/craftinginterpreters"
  if [[ ! -d "${craftinginterpreters_repo_location}" ]]; then
    git clone "${craftinginterpreters_git_location}" "${craftinginterpreters_repo_location}"
  else
    echo "Repo already exists at '${craftinginterpreters_repo_location}'."
  fi

  build_interpreters

  jlox_jar="${REPO_ROOT}/bazel-bin/books/crafting_interpreters/jlox/lox/Lox_deploy.jar"
  jlox_exe="$(create_temp_jlox_exe_script "${jlox_jar}")"
  chmod +x "${jlox_exe}"

  pushd "${craftinginterpreters_repo_location}"
  make get
  # TODO(Jonathon): Fork 'munificent/craftinginterpreters' to improve test suite UX.
  # Test runner doesn't display expected error properly. The regex checks for
  # '[line 9] ...' but the reporting shows '[9] ...'.
  # It's caused by this source code line: _expectedErrors.add("[$lineNum] ${match[1]}");
  dart tool/bin/test.dart jlox --interpreter "$jlox_exe"
  popd

  popd
}

main "$@"

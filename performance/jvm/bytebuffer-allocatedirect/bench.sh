#!/usr/bin/env bash

set -euo pipefail

REPO_DIR=$(git rev-parse --show-toplevel)
# shellcheck disable=SC1090
source "${REPO_DIR}/performance/jvm/bytebuffer-allocatedirect/_common.sh"

main() {
  bazel build //performance/jvm/bytebuffer-allocatedirect:benchmarks_deploy.jar

  local args=()
  for arg; do
    case "${arg}" in
      alloc1)
        args+=( "me.serce.AllocateBuffer1" )
        ;;
      alloc2)
        args+=( -wi 1 -r 120 -p size=128 "me.serce.AllocateBuffer1.direct" )
        ;;
      alloc3)
        args+=( -wi 1 -r 120 -p size=128 "me.serce.AllocateBuffer1.heap" )
        ;;
      alloc4)
        args+=( "me.serce.AllocateBuffer2" )
        ;;
      copy)
        args+=( "me.serce.CopyFileBenchmark.copyFiles" )
        ;;
      access)
        args+=( "me.serce.BufferAccessBenchmark.putLong" )
        ;;
      reverse)
        args+=( "me.serce.CopyFileBenchmark.reverseBytesInFiles" )
        ;;
      order)
        args+=( "me.serce.OrderBenchmark.sumBytes" )
        ;;
      *)
        args+=( "${arg}" )
        ;;
    esac
  done

  info "Starting " "${args[@]}"
  benchmarks_target_deploy_jar="bazel-bin/performance/jvm/bytebuffer-allocatedirect/bench/src/main/java/me/serce/benchmarks_deploy.jar"
  # Shutdown Bazel for it to not interfere with the benchmark.
  bazel shutdown
  java -jar "${benchmarks_target_deploy_jar}" "${args[@]}"
}

main "$@"

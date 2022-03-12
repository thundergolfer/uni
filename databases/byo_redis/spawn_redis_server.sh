#!/bin/sh

set -e

main() {
  tmpFile=$(mktemp -d)
  source_files="$(find . -name "*.java" | grep -v "Test" | xargs echo)"
  javac -d "$tmpFile" $source_files
  jar cf java_redis.jar -C "$tmpFile"/ .
  exec java -cp java_redis.jar com.thundergolfer.uni.byo.redis.Main "$@"
}

main "$@"

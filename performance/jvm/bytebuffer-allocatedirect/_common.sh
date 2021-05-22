PROG=$(basename "$0")

info() {
  echo "$(date '+[%Y-%m-%d %H:%M:%S]') ${PROG}: INFO: $@"
}

error() {
  echo "$(date '+[%Y-%m-%d %H:%M:%S]') ${PROG}: ERROR: $@"
  exit 1
}

"""
The metrics server module is responsible for 'online monitoring'.
It will consume the schema'd events being persisted to logs by the various
servers in this application, and track certain metrics over time, such as
'number of users marking an email as spam in the last 5 minutes'.
"""
import collections
import os
import pathlib
import time

# The queues really shouldn't become very large. A low max
# helps us surface bugs.
QUEUE_MAX_LEN = 1000
FOO_METRIC_QUEUE = collections.deque(maxlen=QUEUE_MAX_LEN)


def track_foo_metric(event, epoch_instant: int) -> None:
    # NOTE: for the moment the 'event' is just an epoch time as
    # an integer. makes for easy direct comparison.
    global FOO_METRIC_QUEUE
    metric_window_len_secs = 10
    window_left = epoch_instant - 10
    print(event)
    if len(FOO_METRIC_QUEUE) > 0:
        head = FOO_METRIC_QUEUE[-1]
        curr = FOO_METRIC_QUEUE[0]
        while curr < window_left:
            _ = FOO_METRIC_QUEUE.popleft()
            if curr == head:
                break  # don't remove more than exists in deque
            else:
                curr = FOO_METRIC_QUEUE[0]
    FOO_METRIC_QUEUE.append(int(event))
    print(f"foo_metric val: {len(FOO_METRIC_QUEUE)}")


def follow(log_path: pathlib.Path):
    log_file = open(log_path, "r")
    # seek the end of the file
    log_file.seek(0, os.SEEK_END)

    # start infinite loop
    while True:
        # read last line of file
        line = log_file.readline()
        # sleep if file hasn't been updated
        if not line:
            time.sleep(0.1)
            continue
        yield line


if __name__ == "__main__":
    # NOTE: Testing with 'echo "$(date +%s)" >> foo.txt'
    log_path = "/Users/jonathon/Code/thundergolfer/uni/machine_learning/applications/spam/a_plan_for_spam/foo.txt"
    log_lines = follow(log_path=log_path)
    for l in log_lines:
        track_foo_metric(event=l, epoch_instant=int(time.time()))

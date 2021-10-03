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

from typing import Callable

# The queues really shouldn't become very large. A low max
# helps us surface bugs.
QUEUE_MAX_LEN = 1000
EMAIL_SPAM_FILTERED_METRIC_QUEUE = collections.deque(maxlen=QUEUE_MAX_LEN)

CounterMetricFunc = Callable[[str, int], None]


def build_email_spam_filtered_counter_function(
    metric_window_size_secs: int,
) -> CounterMetricFunc:
    def track_email_spam_metric(event_str: str, epoch_instant: int) -> None:
        # NOTE: for the moment the 'event' is just an epoch time as
        # an integer. makes for easy direct comparison.
        global EMAIL_SPAM_FILTERED_METRIC_QUEUE
        window_left = epoch_instant - 10
        if len(EMAIL_SPAM_FILTERED_METRIC_QUEUE) > 0:
            head = EMAIL_SPAM_FILTERED_METRIC_QUEUE[-1]
            curr = EMAIL_SPAM_FILTERED_METRIC_QUEUE[0]
            while curr < window_left:
                _ = EMAIL_SPAM_FILTERED_METRIC_QUEUE.popleft()
                if curr == head:
                    break  # don't remove more than exists in deque
                else:
                    curr = EMAIL_SPAM_FILTERED_METRIC_QUEUE[0]
        # TODO: Should be event's timestamp not epoch_instance
        EMAIL_SPAM_FILTERED_METRIC_QUEUE.append(epoch_instant)
        if epoch_instant % 10 == 0:
            print(
                f"email_spam_filtered count in last {metric_window_size_secs} seconds: {len(EMAIL_SPAM_FILTERED_METRIC_QUEUE)}"
            )

    return track_email_spam_metric


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
    time.sleep(2)  # Wait for logs to become available
    # NOTE: Testing with 'echo "$(date +%s)" >> foo.txt'
    log_path = pathlib.Path(
        "/Users/jonathon/Code/thundergolfer/uni/machine_learning/applications/spam/a_plan_for_spam/logs/email_spam_filtered.log"
    )
    log_lines = follow(log_path=log_path)
    func = build_email_spam_filtered_counter_function(metric_window_size_secs=30)
    for l in log_lines:
        func(event_str=l, epoch_instant=int(time.time()))
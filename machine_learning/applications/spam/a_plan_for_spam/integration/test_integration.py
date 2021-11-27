import multiprocessing
import os
import sys
import time
import unittest.mock

import mail_server
import metrics_server
import spam_detect_server
import mail_traffic_simulation


def test_end_to_end(tmp_path):
    os.environ["LOGGING_FILE_PATH_ROOT"] = str(tmp_path)

    num_emails_to_send = 3
    mail_server_proc = multiprocessing.Process(
        target=mail_server.serve,
        args=(),
    )
    mail_server_proc.start()
    metrics_server_proc = multiprocessing.Process(target=metrics_server.run, args=())
    metrics_server_proc.start()
    spam_detect_server_proc = multiprocessing.Process(
        target=spam_detect_server.serve, kwargs={"testing": True}
    )
    spam_detect_server_proc.start()
    with unittest.mock.patch("sys.argv", sys.argv[:1]):
        receivers_simulator_proc = multiprocessing.Process(
            target=mail_traffic_simulation.main, args=(["receivers"],)
        )
        receivers_simulator_proc.start()
        senders_simulator_proc = multiprocessing.Process(
            target=mail_traffic_simulation.main,
            args=(["senders", f"--max-emails={num_emails_to_send}"],),
        )

        senders_simulator_proc.start()

    time.sleep(1)

    senders_simulator_proc.join()
    # The servers processes will never return on their own.
    mail_server_proc.terminate()
    spam_detect_server_proc.terminate()
    metrics_server_proc.terminate()
    receivers_simulator_proc.terminate()

    # Mail sender process must have exit successfully.
    assert senders_simulator_proc.exitcode == 0

    # The EMAIL_VIEWED event is created by the mail receivers simulator process
    # when an email is processed.
    # We check that the number of EMAIL_VIEWED events is equal to the number of sent
    # emails.
    email_viewed_log_file = tmp_path / "email_viewed.log"
    num_email_viewed_events = sum(1 for _ in open(email_viewed_log_file))
    assert num_emails_to_send == num_email_viewed_events

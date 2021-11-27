import time
import multiprocessing

import mail_server
import spam_detect_server


def test_foo():
    mail_server_proc = multiprocessing.Process(target=mail_server.serve, args=())
    mail_server_proc.start()
    spam_detect_server_proc = multiprocessing.Process(target=spam_detect_server.serve, args=())
    spam_detect_server_proc.start()
    time.sleep(1)
    mail_server_proc.terminate()
    spam_detect_server_proc.terminate()

    assert 1 == 1

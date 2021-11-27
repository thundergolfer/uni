import time
import multiprocessing

import mail_server
import metrics_server
import spam_detect_server
import mail_traffic_simulation


def test_foo():
    mail_server_proc = multiprocessing.Process(target=mail_server.serve, args=())
    mail_server_proc.start()
    metrics_server_proc = multiprocessing.Process(target=metrics_server.run, args=())
    metrics_server_proc.start()
    spam_detect_server_proc = multiprocessing.Process(target=spam_detect_server.serve, args=())
    spam_detect_server_proc.start()
    receivers_simulator_proc = multiprocessing.Process(target=mail_traffic_simulation.main, args=())
    receivers_simulator_proc.start()

    time.sleep(1)

    mail_server_proc.terminate()
    spam_detect_server_proc.terminate()
    metrics_server_proc.terminate()
    receivers_simulator_proc.terminate()  # TODO: change to join()

    assert 1 == 1

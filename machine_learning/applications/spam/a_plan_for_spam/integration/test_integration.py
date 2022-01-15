import json
import multiprocessing
import os
import pathlib
import sys
import time
import unittest.mock

import mail_server
import metrics_server
import spam_detect_server
import mail_traffic_simulation
from datasets.enron import dataset


# TODO(Jonathon): Should write a test which checks a UTF-8 email can make it end-to-end.


def test_end_to_end(tmp_path):
    tmp_datasets_root = tmp_path / "datasets"
    tmp_datasets_root.mkdir()
    tmp_logs_path = tmp_path / "logs"
    tmp_logs_path.mkdir()
    tmp_test_dataset_subpath = "test_dataset.json"
    os.environ["DATASETS_PATH_ROOT"] = str(tmp_datasets_root)
    os.environ["DATASET_SUBPATH"] = tmp_test_dataset_subpath
    os.environ["LOGGING_FILE_PATH_ROOT"] = str(tmp_logs_path)

    test_dataset = {
        "<ef6a01c57ba8$bf4d21ab$a599a22a@about-inc.com>": dataset.Example(
            email='Received: from 177-227-60-61-pktv-2w.tinp.net.tw (HELO 61.60.227.177) (61.60.227.177)\n  by '
                  'projecthoneypotmailserver with SMTP; 28 Jun 2005 06:21:29 -0000\nMessage-ID: '
                  '<ef6a01c57ba8$bf4d21ab$a599a22a@about-inc.com>\nFrom: Vanessa J. Smith '
                  '<34kianusch@about-inc.com>\nTo: projecthoneypot@projecthoneypot.org\nSubject: '
                  '=?iso-8859-1?B?QWRvYmUgQWNyb2JhdCA2LjAgLSB3aG9sZXNhbGUgcHJpY2U=?=\nDate: Tue, 28 Jun 2005 06:11:52 '
                  '+0000\nMIME-Version: 1.0\nContent-Type: multipart/related;\n    type="multipart/alternative";\n    '
                  'boundary="----=_NextPart_000_0000_3FC59535.FD306D88"\nX-Priority: 3\nX-MSMail-Priority: '
                  'Normal\nX-Mailer: Microsoft Outlook Express V6.00.2900.2180\nX-MimeOLE: Produced By Microsoft '
                  'MimeOLE V6.00.2900.2180\n\nThis is a multi-part message in MIME '
                  'format.\n\n------=_NextPart_000_0000_3FC59535.FD306D88\nContent-Type: multipart/alternative;\n    '
                  'boundary="----=_NextPart_001_0001_556EE622.2D98BC29"\n\n\n------=_NextPart_001_0001_556EE622'
                  '.2D98BC29\nContent-Type: text/plain;\n    charset="iso-8859-1"\nContent-Transfer-Encoding: '
                  '7bit\n\n     Get access to all the software imaginable for less!\nWe sell software 2-6 times '
                  'cheaper than retail price.\n\nExamples:\n$79.95 Windows XP Professional (Including: Service Pack '
                  '2)\n$89.95 Microsoft Office 2003 Professional / $79.95 Office XP Professional\n$99.95 Adobe '
                  'Photoshop 8.0/CS (Including: ImageReady CS)\n$179.95 Macromedia Studio MX 2004 (Including: '
                  'Dreamweaver MX + Flash MX\n+ Fireworks MX)\n$79.95 Adobe Acrobat 6.0 Professional\n$69.95 Quark '
                  'Xpress 6 Passport Multilanguage\n\nSpecial Offers:\n$89.95 Windows XP Professional + Office XP '
                  'Professional\n$149.95 Adobe Creative Suite Premium (5 CD)\n$129.95 Adobe Photoshop 7 + Adobe '
                  'Premiere 7 + Adobe Illustrator 10\n\nAll main products from Microsoft, Adobe, Macromedia, Corel, '
                  'etc.\nAnd many more... Go visit us at:\n\nhttp://www.softdisks-ltd.com\n\nRegards,'
                  '\nVanessa Smith\n\n\n_____________________________________________________ \nTo be taken off '
                  'future campaigns, go: '
                  'http://www.softdisks-ltd.com/uns.htm\n_____________________________________________________ \n\n '
                  '\n------=_NextPart_001_0001_556EE622.2D98BC29\nContent-Type: text/html;\n    '
                  'charset="iso-8859-1"\nContent-Transfer-Encoding: 7bit\n\n<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML '
                  '4.0 Transitional//EN">\n<HTML><HEAD>\n<META http-equiv=Content-Type content="text/html; '
                  'charset=iso-8859-1">\n<META content="MSHTML 6.00.2900.2604" '
                  'name=GENERATOR></HEAD>\n<BODY>\n<CENTER>\n<TABLE cellSpacing=0 cellPadding=0 width=800 '
                  'align=center border=0>\n  <TBODY>\n  <TR>\n    <TD>Get access to all the software imaginable for '
                  '\n      less!<BR>We sell software 2-6 times cheaper than retail \n      '
                  'price.<BR><BR>Examples:<BR>$79.95 Windows XP Professional (Including: Service Pack \n      '
                  '2)<BR>$89.95 Microsoft Office 2003 Professional / $79.95 Office \n      XP Professional<BR>$99.95 '
                  'Adobe Photoshop 8.0/CS (Including: ImageReady \n      CS)<BR>$179.95 Macromedia Studio MX 2004 ('
                  'Including: Dreamweaver MX + \n      Flash MX + Fireworks MX)<BR>$79.95 Adobe Acrobat 6.0 \n      '
                  'Professional<BR>$69.95 Quark Xpress 6 Passport Multilanguage<BR><BR>Special Offers:<BR>$89.95 '
                  'Windows \n      XP Professional + Office XP Professional<BR>$149.95 Adobe Creative Suite Premium ('
                  '5 CD)<BR>$129.95 Adobe Photoshop 7 + Adobe \n      Premiere 7 + Adobe Illustrator 10<BR><BR>All '
                  'main products from Microsoft, \n      Adobe, Macromedia, Corel, etc.<BR>And many more... Go visit '
                  'us at:<BR><BR><A \n      href="http://www.softdisks-ltd.com">http://www.softdisks-ltd.com</A><BR'
                  '><BR>Regards,<BR>Vanessa Smith<BR><BR><BR>_____________________________________________________ \n '
                  '     <BR>To be taken off future campaigns, go: <A \n      '
                  'href="http://www.softdisks-ltd.com/uns.htm">http://www.softdisks-ltd.com/uns.htm</A><BR'
                  '>_____________________________________________________ \n\n      '
                  '<P></P></TD></TR></TBODY></TABLE></CENTER></BODY></HTML>\n\n------=_NextPart_001_0001_556EE622'
                  '.2D98BC29--\n\n\n\n------=_NextPart_000_0000_3FC59535.FD306D88--\n\u0000\n',
            spam=False,
        ),
    }
    full_test_dataset_path: pathlib.Path = tmp_datasets_root / tmp_test_dataset_subpath
    full_test_dataset_path.write_text(json.dumps(test_dataset))

    num_emails_to_send = len(test_dataset)
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
    email_viewed_log_file = tmp_logs_path / "email_viewed.log"
    num_email_viewed_events = sum(1 for _ in open(email_viewed_log_file))
    assert num_emails_to_send == num_email_viewed_events

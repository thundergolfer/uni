import mail_traffic_simulation


def test_extract_email_header_field():
    expected = "service@paypal.com"
    example_email = """Received: from 72-29-76-63.dimenoc.com (HELO dime94.dizinc.com) (72.29.76.63)
  by projecthoneypotmailserver with SMTP; 22 Jun 2005 15:35:40 -0000
Received: from localhost ([127.0.0.1]:50048 helo=www.heroscape.net)
	by dime94.dizinc.com with esmtp (Exim 4.50)
	id 1Dl7GM-0004M2-Kq
	for projecthoneypot@projecthoneypot.org; Wed, 22 Jun 2005 11:35:38 -0400
Date: Wed, 22 Jun 2005 11:35:38 -0400
To: "projecthoneypot@projecthoneypot.org" <projecthoneypot@projecthoneypot.org>
From: "service@paypal.com" <service@paypal.com>
Subject: Your Account Hass Ben Limited
Message-ID: <055b39766690c783eeb423b3d1ecfdf7@www.heroscape.net>
X-Priority: 3
X-Mailer: PHPMailer [version 1.72]
MIME-Version: 1.0
Content-Transfer-Encoding: 8bit
Content-Type: text/html; charset="iso-8859-1"
X-AntiAbuse: This header was added to track abuse, please include it with any abuse report
X-AntiAbuse: Primary Hostname - dime94.dizinc.com
X-AntiAbuse: Original Domain - tiggersdontlike.mcmike.org
X-AntiAbuse: Originator/Caller UID/GID - [47 12] / [47 12]
X-AntiAbuse: Sender Address Domain - paypal.com

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<body>
</body 
"""
    from_val = mail_traffic_simulation.extract_email_from(
        email_bytes=example_email.encode("utf-8"),
    )
    assert expected == from_val

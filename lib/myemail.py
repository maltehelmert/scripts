# -*- coding: utf-8 -*-

from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# compatibility code Python2/Python3
try:
    str
except NameError:
    str = str

def send_email(to_address, subject, contents,
               from_address="Malte Helmert <malte.helmert@posteo.de>",
               attachments={}, host="localhost"):
    """Send an e-mail to <to_address> with subject <subject> and message
    body <contents>. The <from_address> argument can be used to set the
    sender of the message, but normally the default should be used.
    Tuples (NAME, ADDR) may be passed in for either address to obtain an
    address like 'NAME <ADDR>' with the proper escaping.
    The <attachments> argument, if used, should be a dictionary with pairs of
    the form (filename, contents). Content type MIME/text is assumed.

    Example: send_email('Malte Helmert <malte.helmert@posteo.de>',
        'Test Message', 'No interesting text here.')"""

    from_address = make_address(from_address)
    to_address = make_address(to_address)

    text_part = MIMEText(contents.encode("utf-8"), "plain", "utf-8")
    if attachments:
        email = MIMEMultipart()
        email.attach(text_part)
        for filename, text in sorted(attachments.items()):
            attachment = MIMEText(text.encode("utf-8"), "plain", "utf-8")
            attachment.add_header("Content-Disposition", "attachment",
                                  filename=filename)
            email.attach(attachment)
    else:
        email = text_part
    email["From"] = from_address
    email["To"] = to_address
    email["Subject"] = subject

    server = smtplib.SMTP()
    server.connect(host)
    server.sendmail(email["From"], [email["To"]], email.as_string())
    server.close()

def make_address(arg):
    if isinstance(arg, str):
        return arg
    else:
        return formataddr(arg)

import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


class MailSender(object):

    def __init__(self, host, port, password=None):
        self.host = host
        self.port = port
        self.password = password

    def send(self, from_address, to_address, subject, body, attachments=None, cc_addresses=None, bcc_addresses=None,):
        if attachments:
            msg = self.create_body_with_attachment(
                from_address, to_address, subject, body, attachments, cc_addresses, bcc_addresses)
        else:
            msg = self.create_body(from_address, to_address, subject, body, cc_addresses, bcc_addresses)

        send_list = [to_address]

        if cc_addresses:
            if type(cc_addresses) is list:
                send_list = send_list + cc_addresses
            else:
                send_list = send_list + [cc_addresses]

        if bcc_addresses:
            if type(cc_addresses) is list:
                send_list = send_list + bcc_addresses
            else:
                send_list = send_list + [bcc_addresses]

        smtpobj = smtplib.SMTP(self.host, self.port)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        if self.password:
            smtpobj.login(from_address, self.password)
        smtpobj.sendmail(from_address, send_list, msg.as_string())
        smtpobj.close()

    @staticmethod
    def create_body_with_attachment(from_address, to_address, subject, body, attachments, cc_addresses=None,
                                    bcc_addresses=None):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = to_address

        if bcc_addresses is not None and len(bcc_addresses) != 0:
            msg['Bcc'] = ','.join(bcc_addresses)
        if cc_addresses is not None and len(cc_addresses) != 0:
            msg['cc'] = ','.join(cc_addresses)

        msg['Date'] = formatdate()
        body = MIMEText(body.encode("utf-8"), 'html', 'utf-8')
        msg.attach(body)

        if type(attachments) is not list:
            attachments = [attachments]

        for attachment in attachments:
            base_name = os.path.basename(attachment)
            with open(attachment, "rb") as f:
                part = MIMEApplication(
                    f.read(),
                    Name=base_name
                )

            part['Content-Disposition'] = 'attachment; filename="{}"'.format(base_name)
            msg.attach(part)

        return msg

    @staticmethod
    def create_body(from_address, to_address, subject, body, cc_addresses=None, bcc_addresses=None):
        msg = MIMEText(body.encode("utf-8"), 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = to_address

        if bcc_addresses is not None and len(bcc_addresses) != 0:
            msg['Bcc'] = ','.join(bcc_addresses)
        if cc_addresses is not None and len(cc_addresses) != 0:
            msg['cc'] = ','.join(cc_addresses)

        msg['Date'] = formatdate()

        return msg

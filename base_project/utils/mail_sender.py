import copy
import os
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from typing import Union


class MailSender(object):
    """
    メール送信を行うクラス
    """

    def __init__(self, smtp_host: str, smtp_port: int, user: str = None, password: str = None):
        """コンストラクタ

        Args:
            smtp_host: smtpのホスト
            smtp_port: smtpのポート
            user: ユーザ
            password: パスワード
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.user = user
        self.password = password

    def send(self, from_address: str, to_addresses: Union[str, list], subject: str, body: str,
             attachments: Union[str, list] = None, profile: str = None, cc_addresses: Union[str, list] = None,
             bcc_addresses: Union[str, list] = None):
        """メールを送信する

        Args:
            from_address: 送信元アドレス
            to_addresses: 送信先アドレス
            subject: 件名
            body: 本文
            attachments: 添付ファイル
            profile: プロファイル
            cc_addresses: ccアドレス
            bcc_addresses:　bccアドレス

        """

        if attachments:
            msg = self.create_body_with_attachment(
                from_address, to_addresses, subject, body, attachments, profile, cc_addresses, bcc_addresses)
        else:
            msg = self.create_body(from_address, to_addresses, subject, body, profile, cc_addresses, bcc_addresses)

        if type(to_addresses) is list:
            send_list = copy.copy(to_addresses)
        else:
            send_list = [to_addresses]

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

        smtpobj = smtplib.SMTP(self.smtp_host, self.smtp_port)
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.ehlo()
        if self.password:
            smtpobj.login(self.user, self.password)
        smtpobj.sendmail(from_address, send_list, msg.as_string())
        smtpobj.close()

    def create_body_with_attachment(self, from_address, to_addresses, subject, body, attachments, profile,
                                    cc_addresses=None, bcc_addresses=None):
        """添付ファイル付きのメール本文を作成する

        Args:
            from_address: 送信元アドレス
            to_addresses: 送信先アドレス
            subject: 件名
            body: 本文
            attachments: 添付ファイル
            profile: プロファイル
            cc_addresses: ccアドレス
            bcc_addresses:　bccアドレス

        Returns:
            メール本文
        """

        msg = MIMEMultipart()
        msg = self.create_msg(msg, from_address, to_addresses, subject, profile, cc_addresses, bcc_addresses)
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

    def create_body(self, from_address, to_addresses, subject, body, profile, cc_addresses=None, bcc_addresses=None):
        """メール本文を作成する

        Args:
            from_address: 送信元アドレス
            to_addresses: 送信先アドレス
            subject: 件名
            body: 本文
            profile: プロファイル
            cc_addresses: ccアドレス
            bcc_addresses:　bccアドレス

        Returns:
            メール本文
        """

        msg = MIMEText(body.encode("utf-8"), 'html', 'utf-8')
        return self.create_msg(msg, from_address, to_addresses, subject, profile, cc_addresses, bcc_addresses)

    @staticmethod
    def create_msg(msg, from_address, to_addresses, subject, profile=None, cc_addresses=None, bcc_addresses=None):
        msg['Subject'] = subject
        if profile:
            msg['From'] = '{} <{}>'.format(Header(profile.encode('utf-8'), 'utf-8').encode(), from_address)
        else:
            msg['From'] = from_address

        def to_string_addresses(addresses):
            if type(addresses) is list:
                return ','.join(addresses)
            else:
                return addresses

        msg['To'] = to_string_addresses(to_addresses)
        msg['Bcc'] = to_string_addresses(bcc_addresses)
        msg['Cc'] = to_string_addresses(cc_addresses)

        msg['Date'] = formatdate()

        return msg

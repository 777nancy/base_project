import os

from jinja2 import Environment, BaseLoader

from base_project import config
from base_project.utils import mail_sender, template_file_reader


class Mail(object):

    def __init__(self, address_id):
        self._mail_config_reader = config.MailConfigReader()

        self._address_id = address_id

    def send(self, subject_id, body_file_path, attachments=None, subject_params=None, body_params=None):
        _config = config.Config.get_instance()

        _template_file_reader = template_file_reader.TemplateFileReader(
            _config.TEMPLATES_ROOT_PATH)

        subject = self._mail_config_reader.get_subject_by_id(subject_id)
        if subject_params:
            env = Environment(loader=BaseLoader())
            subject = env.from_string(self._mail_config_reader.get_subject_by_id(subject_id))
            subject = subject.render(subject_params)

        body = _template_file_reader.read(body_file_path, body_params)

        from_address, to_addresses, profile, cc_addresses, bcc_addresses = self._mail_config_reader.get_addresses_by_id(
            self._address_id)

        _mail_sender = mail_sender.MailSender(**_config.MAIL_CONFIG)

        _mail_sender.send(from_address, to_addresses, subject, body, attachments, profile, cc_addresses, bcc_addresses)

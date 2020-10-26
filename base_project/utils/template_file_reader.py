import os
import string


class TemplateFileReader(object):

    def __init__(self, root_dir: str, encoding: str = 'utf-8'):
        self._root_dir = root_dir
        self._encoding = encoding

    def read(self, file_path, context=None):
        with open(os.path.join(self._root_dir, file_path), mode='r', encoding=self._encoding) as fin:
            content = fin.read()

        if context:
            template = string.Template(context)
            content = template.safe_substitute(context)

        return content

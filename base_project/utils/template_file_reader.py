import os

from jinja2 import Environment, FileSystemLoader


class TemplateFileReader(object):

    def __init__(self, root_dir: str = None, encoding: str = 'utf-8'):
        self._env = Environment(loader=FileSystemLoader(root_dir, encoding=encoding))

    def read(self, file_path, context=None):

        if os.name == 'nt':
            file_path = file_path.replace(os.path.sep, '/')

        content = self._env.get_template(file_path)
        if context:
            return content.render(context)
        else:
            return content.render()

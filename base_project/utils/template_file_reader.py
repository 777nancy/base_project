from jinja2 import Environment, FileSystemLoader


class TemplateFileReader(object):

    def __init__(self, root_dir: str = None, encoding: str = 'utf-8'):
        self._env = Environment(loader=FileSystemLoader(root_dir, encoding=encoding))

    def read(self, file_path, context=None):
        content = self._env.get_template(file_path)
        if context:
            return content.render(context)
        else:
            return content.render()

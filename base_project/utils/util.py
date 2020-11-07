import traceback


def exception2str(exception):
    return ''.join(traceback.TracebackException.from_exception(exception).format())


def name2base_name(name):
    return name.split('.')[-1]

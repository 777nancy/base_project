import traceback


def exception2str(exception):
    return ''.join(traceback.TracebackException.from_exception(exception).format())

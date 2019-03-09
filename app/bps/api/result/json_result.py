import functools
import sys

from flask import jsonify

from .code import ResultCode


class DictMixin(dict):

    __dict_mixin_exclude__ = None

    def __setitem__(self, key, value):
        if self.__is_include(key):
            object.__setattr__(self, key, value)

        super().__setitem__(key, value)

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)

        if self.__is_include(key):
            super().__setitem__(key, value)

    def __is_include(self, key):
        return not self.__dict_mixin_exclude__ or key not in self.__dict_mixin_exclude__


class JSONResult(DictMixin):

    __dict_mixin_exclude__ = ('code',)
    __slots__ = ('result_code', 'result_message', 'data', 'exception_info')

    def __init__(self, code: ResultCode=ResultCode.OK, msg=None,
                 data=None, exception: Exception=None):

        super().__init__()

        data = data or {}
        self.result_code = code.value
        self.result_message = msg or code.name
        self.data = data

        if exception:
            self.exception_info = ExceptionInfo(exception)

    @property
    def code(self):
        return ResultCode(self.result_code)

    @code.setter
    def code(self, v):
        self.result_code = v.value
        self.result_message = v.name


class ExceptionInfo(DictMixin):

    __slots__ = ('exc_type', 'exc_message')

    def __init__(self, exception: Exception=None):
        super().__init__()

        if exception is None:
            _, exception, _ = sys.exc_info()

        self.exc_type = None
        self.exc_message = None
        self.set_exception(exception)

    def set_exception(self, v: Exception):
        if v is None:
            return

        self.exc_type = v.__class__.__name__

        if len(v.args) == 1:
            message = v.args[0]
        else:
            message = ''.join(v.args)

        self.exc_message = message


def json_result(func):

    @functools.wraps(func)
    def wrapper(*args, **kw):

        result: JSONResult = func(*args, **kw)

        response = jsonify(result)
        response.status_code = result.result_code // 100

        return response

    return wrapper

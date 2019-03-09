from enum import Enum


class ResultCode(Enum):
    OK = 0

    INVALID_FORM = 40001
    INCORRECT_USERNAME = 40002

    USER_NOT_EXISTS = 40301
    INCORRECT_PASSWORD = 40302

    ALREADY_REGISTERED = 40901
    ALREADY_LOGGED_IN = 40902

    UNHANDLED_EXCEPTION = 50001


def result_code_map():
    code = {}

    for each in ResultCode.__members__:
        code[each] = ResultCode[each].value

    return code

import typing
import datetime

now: typing.Callable = datetime.datetime.now


def get_now_with_format(format_string: str = '%Y%m%d%H%M%S') -> str:
    return now().strftime(format_string)

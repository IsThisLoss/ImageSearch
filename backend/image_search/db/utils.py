import dataclasses
import time
import typing


def as_dict(data: typing.Any) -> dict:
    result = {}
    for key, value in dataclasses.asdict(data).items():
        if value is None:
            continue
        result[key] = value
    return result


def now() -> int:
    return int(time.time())

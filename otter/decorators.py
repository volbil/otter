from .constants import BAD_REQUEST
from marshmallow import Schema
from functools import wraps

def use_args(schema_args, error=BAD_REQUEST):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            schema = Schema.from_dict(schema_args)

            try:
                schema().load(args[1])
            except Exception:
                return error

            return function(*args, **kwargs)

        return wrapper

    return decorator

import logging

def debug(function, name):
    def wrapper(*args, **kwargs):
        logging.info(f"Running {name}")
        return function(*args, **kwargs)

    return wrapper

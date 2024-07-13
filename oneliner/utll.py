import re


def camel_to_snake(camel):
    s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', camel)
    return s1.lower()


def stringify(value):
    if value is None:
        return "nil"
    elif isinstance(value, bool):
        return str(value).lower()
    else:
        return str(value)


def is_truthy(object):
    if object is None:
        return False
    if isinstance(object, bool):
        return object
    if isinstance(object, float):
        return object != 0
    if isinstance(object, int):
        return object != 0
    return True

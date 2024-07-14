import re


def camel_to_snake(camel):
    s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', camel)
    return s1.lower()


def stringify(value, for_debug=False):
    match(value):
        case None:
            return "nil"
        case str():
            if for_debug:
                return f'"{value}"'
            else:
                return value
        case bool():
            return str(value).lower()
        case list():
            return ("[" +
                    ", ".join([stringify(item, True) for item in value])
                    + "]")
        case dict():
            return ("%{" +
                    ", ".join(
                        [f"{stringify(k, True)}: {stringify(v, True)}"
                         for k, v in value.items()])
                    + "}")
        case _:
            return str(value)


def is_truthy(object):
    match(object):
        case None:
            return False
        case bool():
            return object
        case float():
            return object != 0
        case int():
            return object != 0
        case _:
            return True

import math


def triangle(*args):
    if len(args) != 3:
        return None, "required 3 arguments"
    s = sum(args) / 2
    res = math.sqrt(s * (s - args[0]) * (s - args[1]) * (s - args[2]))
    return round(res, 2), None


def rectangle(*args):
    if len(args) != 2:
        return None, "required 2 arguments"

    res = args[0] * args[1]
    return round(res, 2), None


def square(*args):
    if len(args) != 1:
        return None, "required 1 arguments"

    res = args[0]**2
    return round(res, 2), None


def diamond(*args):
    if len(args) != 2:
        return None, "required 2 arguments"

    res = args[0] * args[1] / 2
    return round(res, 2), None

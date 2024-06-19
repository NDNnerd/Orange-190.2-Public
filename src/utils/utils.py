def format_number(x, decimals=0):
    if decimals == -1:
        return int(format(x, '.0f'))
    return float(format(x, f'.{decimals}f'))

def f(x, d=-1):
    return format_number(x, d)



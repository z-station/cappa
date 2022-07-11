from typing import Any


def checker_runner(
    checker_func: str,
    right_value: Any,
    value: Any
):
    checker_func_vars = {
        'value': value,
        'right_value': right_value
    }
    exec(
        checker_func + '\nresult = checker(right_value, value)',
        globals(),
        checker_func_vars
    )
    return checker_func_vars['result']

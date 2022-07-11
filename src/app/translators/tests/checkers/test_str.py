import pytest
from app.translators.checkers import str_checker
from app.translators.checkers.str_checker import checker
from app.translators.utils import checker_runner


def test__equal__ok():

    # arrange
    right_value = 'test'
    value = 'test'

    # act
    result = checker(
        right_value=right_value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=str_checker,
        right_value=right_value,
        value=value
    )

    # assert
    assert result is True
    assert runner_result is True


def test__multiple_rows__ok():

    """ Проверить, если right_value это несколько значений,
     каждое с новой строки, то сравнивать построчно """

    # arrange
    right_value = 'test\n50'
    value = 'test\n50'

    # act
    result = checker(
        right_value=right_value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=str_checker,
        right_value=right_value,
        value=value
    )

    # assert
    assert result is True
    assert runner_result is True


@pytest.mark.parametrize('value', ('', None, '0'))
def test__empty_values__ok(value):

    # act
    result = checker(
        right_value=value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=str_checker,
        right_value=value,
        value=value
    )

    # assert
    assert result is True
    assert runner_result is True


@pytest.mark.parametrize('value', ('test\n\n1', '0\n0'))
def test__empty_value_in_many_rows__ok(value):

    # act
    result = checker(
        right_value=value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=str_checker,
        right_value=value,
        value=value
    )

    # assert
    assert result is True
    assert runner_result is True


def test__end_new_line__return_false():

    # arrange
    right_value = 'test'
    value = 'test\n'

    # act
    result = checker(
        right_value=right_value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=str_checker,
        right_value=right_value,
        value=value
    )

    # assert
    assert result is False
    assert runner_result is False


def test__format__ok():

    # assert
    assert str_checker.startswith(
        'def checker(right_value: str, value: str) -> bool:'
    )
    assert str_checker.find('return') > 0

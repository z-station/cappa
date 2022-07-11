import pytest
from app.translators.checkers import int_checker
from app.translators.checkers.int_checker import checker
from app.translators.utils import checker_runner


def test__equal__ok():

    # arrange
    right_value = '92'
    value = '92'

    # act
    result = checker(
        right_value=right_value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=int_checker,
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
    right_value = '92\n50'
    value = '92\n50'

    # act
    result = checker(
        right_value=right_value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=int_checker,
        right_value=right_value,
        value=value
    )

    # assert
    assert result is True
    assert runner_result is True


@pytest.mark.parametrize('value', ('92.0', '92.001'))
def test__number_not_integer__return_false(value):

    # act
    result = checker(
        right_value=value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=int_checker,
        right_value=value,
        value=value
    )

    # assert
    assert result is False
    assert runner_result is False


@pytest.mark.parametrize('value', ('[]', 'null', 'one'))
def test__not_number_value__return_false(value):

    # act
    result = checker(
        right_value=value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=int_checker,
        right_value=value,
        value=value
    )

    # assert
    assert result is False
    assert runner_result is False


@pytest.mark.parametrize('value', ('', None, '0'))
def test__empty_values__ok(value):

    # act
    result = checker(
        right_value=value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=int_checker,
        right_value=value,
        value=value
    )

    # assert
    assert result is True
    assert runner_result is True


@pytest.mark.parametrize('value', ('92\n\n1', '0\n0'))
def test__empty_value_in_many_rows__ok(value):

    # act
    result = checker(
        right_value=value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=int_checker,
        right_value=value,
        value=value
    )

    # assert
    assert result is True
    assert runner_result is True


def test__format__ok():

    # assert
    assert int_checker.startswith(
        'def checker(right_value: str, value: str) -> bool:'
    )
    assert int_checker.find('return') > 0

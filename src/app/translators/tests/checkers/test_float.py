import pytest
from app.translators.checkers import float_checker
from app.translators.checkers.float_checker import checker
from app.translators.utils import checker_runner


def test__equal__ok():

    # arrange
    right_value = '92.1'
    value = '92.1'

    # act
    result = checker(
        right_value=right_value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=float_checker,
        right_value=right_value,
        value=value
    )

    # assert
    assert result is True
    assert runner_result is True


def test__not_equal__ok():

    # arrange
    right_value = '92.100001'
    value = '92.1'

    # act
    result = checker(
        right_value=right_value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=float_checker,
        right_value=right_value,
        value=value
    )

    # assert
    assert result is False
    assert runner_result is False


def test__equal__integers__ok():

    # arrange
    right_value = '92'
    value = '92'

    # act
    result = checker(
        right_value=right_value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=float_checker,
        right_value=right_value,
        value=value
    )

    # assert
    assert result is True
    assert runner_result is True


def test__rounding_to_right_value__ok():

    """ Привести кол-во разрядов в дробной часи
        к числу разрядов в дробной части right_value """

    # arrange
    right_value = '92.72'
    value = '92.72000862812729'

    # act
    result = checker(
        right_value=right_value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=float_checker,
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
    right_value = '92.72\n50'
    value = '92.720014\n50'

    # act
    result = checker(
        right_value=right_value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=float_checker,
        right_value=right_value,
        value=value
    )

    # assert
    assert result is True
    assert runner_result is True


def test__value_exponential_form__ok():

    """ Перевести right_value из экспоненциальной в десятичную форму """

    # arrange
    right_value = '12.3456'
    value = '1.234560e+01'

    # act
    result = checker(
        right_value=right_value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=float_checker,
        right_value=right_value,
        value=value
    )

    # assert
    assert result is True
    assert runner_result is True


def test__right_value_exponential_form__ok():

    """ Перевести значение из экспоненциальной в десятичную форму """

    # arrange
    right_value = '1.234560e+01'
    value = '12.3456'

    # act
    result = checker(
        right_value=right_value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=float_checker,
        right_value=right_value,
        value=value
    )

    # assert
    assert result is True
    assert runner_result is True


@pytest.mark.parametrize('value', ('[]', 'null', 'one'))
def test__not_number_value__return_false(value):

    # act
    result = checker(
        right_value=value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=float_checker,
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
        checker_func=float_checker,
        right_value=value,
        value=value
    )

    # assert
    assert result is True
    assert runner_result is True


@pytest.mark.parametrize('value', ('92.01\n\n1.0', '0\n0.0', None))
def test__empty_value_in_many_rows__ok(value):

    # act
    result = checker(
        right_value=value,
        value=value
    )
    runner_result = checker_runner(
        checker_func=float_checker,
        right_value=value,
        value=value
    )

    # assert
    assert result is True
    assert runner_result is True


def test__format__ok():

    # assert
    assert float_checker.startswith(
        'def checker(right_value: str, value: str) -> bool:'
    )
    assert float_checker.find('return') > 0

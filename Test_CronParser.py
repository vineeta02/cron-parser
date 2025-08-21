import pytest
from CronParser import CronParser


@pytest.mark.parametrize("expression,min_value,max_value,expected", [
    ("*", 0, 5, [0, 1, 2, 3, 4, 5]),
    ("3", 0, 5, [3]),
    ("1-4", 0, 5, [1, 2, 3, 4]),
    ("*/2", 0, 5, [0, 2, 4]),
    ("1-5/2", 0, 10, [1, 3, 5]),
    ("3/2", 0, 6, [3, 5]),
    ("1,3,5", 0, 6, [1, 3, 5]),
    ("1,3-4,6/2", 0, 6, [1, 3, 4, 6]),
])
def test_parse_cron_field_basic(expression, min_value, max_value, expected):
    assert CronParser.parse_cron_field(expression, min_value, max_value) == expected


def test_parse_expression_full():
    expression = "*/15 0 1,15 * 1-5 /usr/bin/find"
    parsed = CronParser.parse_expression(expression)

    assert parsed["minute"] == [0, 15, 30, 45]
    assert parsed["hour"] == [0]
    assert parsed["day_of_month"] == [1, 15]
    assert parsed["month"] == list(range(1, 13))
    assert parsed["day of week"] == [1, 2, 3, 4, 5]
    assert parsed["command"] == ["/usr/bin/find"]


def test_invalid_expression_length(capsys):
    expression = "*/15 0 1,15 * /usr/bin/find"
    CronParser.parse_expression(expression)
    captured = capsys.readouterr()
    assert "Cron expression is incorrect! Number of fields in cron expression passed is 5" in captured.out


# ---------------- Edge Cases ---------------- #

def test_duplicate_values_in_comma():
    expr = "1,1,2,3,3"
    result = CronParser.parse_cron_field(expr, 0, 5)
    assert result == [1, 2, 3]  # no duplicates


def test_invalid_range_out_of_bounds():
    expr = "10-20"
    result = CronParser.parse_cron_field(expr, 0, 15)
    assert result == list(range(10, 16))  # capped at max_val


def test_step_larger_than_range():
    expr = "*/20"
    result = CronParser.parse_cron_field(expr, 0, 10)
    assert result == [0]  # only start fits


def test_single_value_step():
    expr = "3/2"
    result = CronParser.parse_cron_field(expr, 0, 5)
    assert result == [3, 5]


def test_day_31_in_february():
    result = CronParser.parse_cron_field("31", 1, 28)
    assert result == []


def test_empty_expression_returns_none():
    with pytest.raises(ValueError):
        CronParser.parse_cron_field("", 0, 10)


def test_non_numeric_input():
    with pytest.raises(ValueError):
        CronParser.parse_cron_field("abc", 0, 10)

def test_zero_or_negative_step():
    with pytest.raises(ValueError):
        CronParser.parse_cron_field("*/0", 0, 59)
    with pytest.raises(ValueError):
        CronParser.parse_cron_field("*/-2", 0, 59)

def test_invalid_range_order():
    with pytest.raises(ValueError):
        CronParser.parse_cron_field("20-10", 0, 59)
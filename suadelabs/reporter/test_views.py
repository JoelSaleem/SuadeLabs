from .views import is_date_valid


def test_date_valid_length():
    '''Tests if incorrect num of . E.g. YYYY-MM-DD-XX'''
    assert is_date_valid('1994-12-11-01') == False
    assert is_date_valid('1994-12') == False
    assert is_date_valid('1994-12-11') == True


def test_validation_year_length():
    '''Tests whether the year is the two digits long'''
    assert is_date_valid('199-12-11') == False
    assert is_date_valid('1994-12-11') == True


def test_validation_month_length():
    '''Tests whether the month is the two digits long'''
    assert is_date_valid('1994-123-11') == False
    assert is_date_valid('1994-12-11') == True


def test_validation_day_length():
    '''Tests whether the day is two digits long'''
    assert is_date_valid('1994-12-1') == False
    assert is_date_valid('1994-12-121') == False
    assert is_date_valid('1994-12-11') == True


def test_validation_date_integers():
    '''Tests whether the year, month and day are integers'''
    assert is_date_valid('AAAA-12-01') == False
    assert is_date_valid('1994-AA-01') == False
    assert is_date_valid('1994-12-AA') == False
    assert is_date_valid('1994-12-01') == True


def test_validation_str_input():
    '''Tests whether the function returns False for incorrect input type'''
    assert is_date_valid(19941211) == False
    assert is_date_valid('1994-12-11') == True

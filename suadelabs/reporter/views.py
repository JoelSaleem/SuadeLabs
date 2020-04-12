from django.http import HttpResponse
from os import path
from json import dumps
from enum import Enum
from .data.data_interface import num_items_sold, num_customers, total_discount,\
    avg_discount_rate, average_order_tot, DataPaths


def is_date_valid(date):
    '''Tests if the date is in the form YYYY-MM-DD. Returns a bool.'''
    if not isinstance(date, str):
        return False

    try:
        year, month, day = date.split('-')
    except ValueError:
        # Can't be split into year, month and day -- not valid
        return False

    try:
        year_invalid = len(year) != 4 or int(year) < 0
        month_invalid = len(month) != 2 or int(month) < 1 or int(month) > 12
        day_invalid = len(day) != 2 or int(day) < 1 or int(day) > 31
    except ValueError:
        # Input cannot be converted to an integer
        return False

    if year_invalid or month_invalid or day_invalid:
        return False

    return True


def index(request, date):
    if not is_date_valid(date):
        return HttpResponse(dumps(
            {'error': 'The date must be a valid date in the form: YYYY-MM-DD'}
        ), status=400)

    data = {}
    data['items'] = int(num_items_sold(date, DataPaths['ORDERS'],
                                       DataPaths['ORDER_LINES']))

    data['customers'] = num_customers(date, DataPaths['ORDERS'])

    data['total_discount_amount'] = total_discount(date, DataPaths['ORDERS'],
                                                   DataPaths['ORDER_LINES'])

    data['discount_rate_avg'] = avg_discount_rate(date, DataPaths['ORDERS'],
                                                  DataPaths['ORDER_LINES'])

    data['order_total_avg'] = average_order_tot(date, DataPaths['ORDERS'],
                                                DataPaths['ORDER_LINES'])

    return HttpResponse(dumps(data))

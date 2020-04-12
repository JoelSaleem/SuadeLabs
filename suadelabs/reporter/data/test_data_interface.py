from os import path
from .data_interface import num_items_sold, num_customers, total_discount,\
    avg_discount_rate, average_order_tot, NoItemsException, get_orders_for_date, \
    get_order_lines_total

TestDataPaths = {
    'COMMSIONS': path.abspath(path.join(__file__, '../test_data/mock_comissions.csv')),
    'ORDER_LINES': path.abspath(path.join(__file__, '../test_data/mock_order_lines.csv')),
    'ORDERS': path.abspath(path.join(__file__, '../test_data/mock_orders.csv')),
    'PRODUCT_PROMOTIONS': path.abspath(path.join(__file__, '../test_data/mock_product_promotions.csv')),
    'PRODUCTS': path.abspath(path.join(__file__, '../test_data/mock_products.csv')),
    'PROMOTIONS': path.abspath(path.join(__file__, '../test_data/mock_promotions.csv')),
}

'''
This file contains tests for interface.py in reporter/data.

The data used in the file can be found in reporter/data/test_data.
'''


def test_get_orders_for_date():
    '''Tests whether the orders for a date can be obtained'''
    orders = get_orders_for_date('2019-08-01', TestDataPaths['ORDERS'])
    assert '2' in orders and '3' in orders
    assert '4' not in orders and '5' not in orders


def test_num_customers():
    '''Tests whether the number of customers can be obtained for a date'''
    assert num_customers('2019-08-01', TestDataPaths['ORDERS']) == 2
    assert num_customers('2019-08-02', TestDataPaths['ORDERS']) == 1
    assert num_customers('2020-08-02', TestDataPaths['ORDERS']) == 0


def test_get_order_lines_total():
    '''
    Tests whether the total for a column (of order_lines) for a date can 
    be obtained from get_order_lines_total()
    '''
    total = get_order_lines_total('2019-08-01', TestDataPaths['ORDERS'],
                                  TestDataPaths['ORDER_LINES'], 'full_price_amount')
    assert total == 6_680_012.0


def test_get_num_items():
    '''
    Tests if get_num_items_sold() returns correct value for
    the total items sold for a particular date
    '''
    num_items = num_items_sold('2019-08-01', TestDataPaths['ORDERS'],
                               TestDataPaths['ORDER_LINES'])

    assert num_items == 154


def test_tot_discount():
    '''
    Tests if total_discount() returns the correct value for the total
    discounted amount for a particular date (to two decimal places)
    '''
    amount = total_discount('2019-08-01', TestDataPaths['ORDERS'],
                            TestDataPaths['ORDER_LINES'])

    assert amount == 4603710.5


def test_avg_discount_rate():
    '''
    Tests if avg_discount_rate() returns correct value for average discounted rate,
    weighted by quantity of items for a particular date (to two decimal places)
    '''
    avg_discount = avg_discount_rate('2019-08-01', TestDataPaths['ORDERS'],
                                     TestDataPaths['ORDER_LINES'])

    assert avg_discount == 0.14

    # No items for date
    avg_discount = avg_discount_rate('2020-08-01', TestDataPaths['ORDERS'],
                                     TestDataPaths['ORDER_LINES'])

    assert avg_discount == 0


def test_average_order_tot():
    '''
    Tests if average_order_tot() returns correct value for avg total
    order for a given date (to two decimal places)
    '''
    value = average_order_tot('2019-08-01', TestDataPaths['ORDERS'],
                              TestDataPaths['ORDER_LINES'])

    assert value == 1_722_903.86

    # No items for date
    value = average_order_tot('2029-08-01', TestDataPaths['ORDERS'],
                              TestDataPaths['ORDER_LINES'])

    assert value == 0

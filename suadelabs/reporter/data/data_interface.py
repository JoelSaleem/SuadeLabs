from os import path

# Paths to data files
DataPaths = {
    'COMMSIONS': path.abspath(path.join(__file__, '../comissions.csv')),
    'ORDER_LINES': path.abspath(path.join(__file__, '../order_lines.csv')),
    'ORDERS': path.abspath(path.join(__file__, '../orders.csv')),
    'PRODUCT_PROMOTIONS': path.abspath(path.join(__file__, '../product_promotions.csv')),
    'PRODUCTS': path.abspath(path.join(__file__, '../products.csv')),
    'PROMOTIONS': path.abspath(path.join(__file__, '../promotions.csv')),
}

# Column numbers in ORDERS file
OrdersColNums = {
    'id': 0,
    'created_at': 1,
    'vendor_id': 2,
    'customer_id': 3
}

# Column numbers in ORDER_LINES file
OrderLinesColNums = {
    'order_id': 0,
    'product_id': 1,
    'product_description': 2,
    'product_price': 3,
    'product_vat_rate': 4,
    'discount_rate':  5,
    'quantity': 6,
    'full_price_amount': 7,
    'discounted_amount': 8,
    'vat_amount_total': 9,
    'total_amount': 10
}


class NoItemsException(Exception):
    '''Raised when no items available for a date'''
    pass


def get_orders_for_date(date, orders_file_path):
    '''
    Get all orders that occur for a certain date

    Args:
        param1 (str): date in the format YYYY-MM-DD
        param2 (str): the path to file containing orders
    '''
    orders = set()
    with open(orders_file_path) as f:
        for line in f:
            if line.strip():
                # If line is not blank
                row = line.split(',')

                order_id_idx = OrdersColNums['id']
                order_id = row[order_id_idx]

                created_at_idx = OrdersColNums['created_at']
                created_at = row[created_at_idx]

                if created_at == 'created_at':
                    # Ignore header row
                    continue

                created_date, _ = created_at.split(' ')
                if date == created_date:
                    orders.add(order_id)

    return orders


def num_customers(date, orders_file_path):
    '''
    Get the number of customers who created orders on a particular date

    Args:
        param1 (str): date in the format YYYY-MM-DD
        param2 (str): the path to file containing orders
    '''
    customers = set()
    with open(orders_file_path) as f:
        for line in f:
            if line.strip():
                # If row is not blank
                row = line.split(',')

                created_at_idx = OrdersColNums['created_at']
                created_at = row[created_at_idx]

                customer_id_idx = OrdersColNums['customer_id']
                customer_id = row[customer_id_idx]

                if created_at == 'created_at' or customer_id == 'customer_id':
                    # Ignore header row
                    continue

                created_date, _ = created_at.split(' ')
                if date == created_date:
                    customers.add(customer_id)

    return len(customers)


def get_order_lines_total(
    date, orders_file_path, order_lines_file_path, col_name
):
    '''
    Get the total for a column in order_lines for a particular date
    (rounded to two decimal places). Returns a float.

    Args:
        param1 (str): date in the format YYYY-MM-DD
        param2 (str): the path to file containing orders
        param3 (str): the path to file containing order_lines
        param4 (str): The column name for the resource in 
                      order_lines file specified
    '''
    orders = get_orders_for_date(date, orders_file_path)
    count = 0

    with open(order_lines_file_path, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                # If line is not blank
                row = line.split(',')
                
                order_id_idx = OrderLinesColNums['order_id']
                order_id = row[order_id_idx]

                target_col_idx = OrderLinesColNums[col_name]
                value = row[target_col_idx]

                if order_id == 'order_id':
                    # Ignore header row
                    continue

                if order_id in orders:
                    count += float(value)

    return round(count, 2)


def num_items_sold(date, orders_file_path, order_lines_file_path):
    '''
    Get number of items sold on a particular day.

    Args:
        param1 (str): date in the format YYYY-MM-DD
        param2 (str): the path to file containing orders
        param3 (str): the path to file containing order_lines
    '''
    num_items = get_order_lines_total(
        date, orders_file_path,
        order_lines_file_path, 'quantity'
    )

    return int(num_items)


def total_discount(date, orders_file_path, order_lines_file_path):
    '''
    Get total discounted amount for a particular date.

    Args:
        param1 (str): date in the format YYYY-MM-DD
        param2 (str): the path to file containing orders
        param3 (str): the path to file containing order_lines
    '''
    tot_discount = get_order_lines_total(
        date, orders_file_path, order_lines_file_path, 'discounted_amount'
    )

    return round(tot_discount, 2)


def avg_discount_rate(date, orders_file_path, order_lines_file_path):
    '''
    Get average discounted rate for a particular date, rounded to 
    two decimal places.

    Args:
        param1 (str): date in the format YYYY-MM-DD
        param2 (str): the path to file containing orders
        param3 (str): the path to file containing order_lines
    '''
    orders = get_orders_for_date(date, orders_file_path)
    total_discount_rate = 0
    num_items = 0

    with open(order_lines_file_path, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                # If line is not blank
                row = line.split(',')

                order_id_idx = OrderLinesColNums['order_id']
                order_id = row[order_id_idx]

                if order_id == 'order_id':
                    # Ignore header row
                    continue

                discount_rate_idx = OrderLinesColNums['discount_rate']
                discount_rate = float(row[discount_rate_idx])

                quantity_idx = OrderLinesColNums['quantity']
                quantity = float(row[quantity_idx])

                if order_id in orders:
                    num_items += quantity
                    total_discount_rate += discount_rate * quantity

    if num_items == 0:
        return 0

    return round(total_discount_rate / num_items, 2)


def average_order_tot(date, orders_file_path, order_lines_file_path):
    '''
    Get average total order amount for a particular date

    Args:
        param1 (str): date in the format YYYY-MM-DD
        param2 (str): the path to file containing orders
        param3 (str): the path to file containing order_lines
    '''
    orders = get_orders_for_date(date, orders_file_path)
    order_total = 0
    with open(order_lines_file_path, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                # If line is not blank
                row = line.split(',')

                order_id_idx = OrderLinesColNums['order_id']
                order_id = row[order_id_idx]
                if order_id == 'order_id':
                    # Ignore header row
                    continue

                total_amount_idx = OrderLinesColNums['total_amount']
                amount = float(row[total_amount_idx])
                if order_id in orders:
                    order_total += amount

    if len(orders) == 0:
        return 0

    return round(order_total / len(orders), 2)

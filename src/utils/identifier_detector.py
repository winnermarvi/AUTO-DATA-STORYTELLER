def is_identifier_column(column_name):

    column_name = column_name.lower()

    identifier_keywords = [
        "id",
        "customerid",
        "customer_id",
        "userid",
        "user_id",
        "orderid",
        "order_id",
        "transactionid",
        "transaction_id",
        "invoiceid",
        "invoice_id",
        "passengerid",
        "passenger_id"
    ]

    return any(
        keyword == column_name
        for keyword in identifier_keywords
    )
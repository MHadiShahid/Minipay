CUSTOMER_BY_ID = """
SELECT
    id,
    customer_ref,
    name,
    created_at
FROM customers
WHERE id = %s;
"""


CREATE_CUSTOMER = """
INSERT INTO customers (customer_ref, name)
VALUES (%s, %s)
RETURNING id, customer_ref, name, created_at;
"""


TRANSACTION_BY_ID = """
SELECT
    id,
    transaction_ref,
    customer_id,
    amount,
    status,
    created_at,
    completed_at,
    failure_code
FROM transactions
WHERE id = %s;
"""


CUSTOMER_TRANSACTIONS = """
SELECT
    id,
    transaction_ref,
    customer_id,
    amount,
    status,
    created_at,
    completed_at,
    failure_code
FROM transactions
WHERE customer_id = %s
ORDER BY created_at DESC;
"""


CREATE_PAYMENT = """
INSERT INTO transactions (
    transaction_ref,
    customer_id,
    amount,
    status,
    created_at
)
VALUES (%s, %s, %s, 'PROCESSING', NOW())
RETURNING
    id,
    transaction_ref,
    customer_id,
    amount,
    status,
    created_at,
    completed_at,
    failure_code;
"""
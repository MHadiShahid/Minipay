import psycopg


TRANSACTION_QUERY = """
SELECT
    t.id,
    t.transaction_ref,
    t.customer_id,
    c.customer_ref,
    c.name,
    t.amount,
    t.status,
    t.created_at,
    t.completed_at,
    t.failure_code
FROM transactions t
JOIN customers c ON c.id = t.customer_id
WHERE t.transaction_ref = %s
ORDER BY t.id;
"""


CALLBACK_QUERY = """
SELECT
    attempt_no,
    http_status,
    callback_status,
    attempted_at
FROM callbacks
WHERE transaction_id = %s
ORDER BY attempt_no;
"""


def get_transaction_data(
    database_url: str,
    transaction_ref: str,
    timeout: int = 5,
):
    with psycopg.connect(
        database_url,
        connect_timeout=timeout,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                TRANSACTION_QUERY,
                (transaction_ref,),
            )
            transactions = cursor.fetchall()

            results = []

            for transaction in transactions:
                cursor.execute(
                    CALLBACK_QUERY,
                    (transaction[0],),
                )
                callbacks = cursor.fetchall()

                results.append(
                    {
                        "transaction": transaction,
                        "callbacks": callbacks,
                    }
                )

    return results

def check_database_health(database_url: str, timeout: int = 5):
    with psycopg.connect(
        database_url,
        connect_timeout=timeout,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()

    return result[0] == 1
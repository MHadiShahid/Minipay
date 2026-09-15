from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .database import get_connection
from .queries import (
    CUSTOMER_BY_ID,
    CREATE_CUSTOMER,
    TRANSACTION_BY_ID,
    CUSTOMER_TRANSACTIONS,
    CREATE_PAYMENT,
)
from .schemas import CustomerCreate, PaymentCreate

app = FastAPI(title="MiniPay API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def transaction_to_dict(row):
    return {
        "id": row[0],
        "transaction_ref": row[1],
        "customer_id": row[2],
        "amount": row[3],
        "status": row[4],
        "created_at": row[5].isoformat(),
        "completed_at": row[6].isoformat() if row[6] else None,
        "failure_code": row[7],
    }


@app.get("/health")
def health_check():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

        return {
            "status": "ok",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "error",
            "database": "unavailable"
        }


@app.post("/api/customers", status_code=201)
def create_customer(customer: CustomerCreate):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    CREATE_CUSTOMER,
                    (customer.customer_ref, customer.name)
                )
                row = cursor.fetchone()

            connection.commit()

        return {
            "id": row[0],
            "customer_ref": row[1],
            "name": row[2],
            "created_at": row[3].isoformat()
        }

    except Exception as exc:
        if "duplicate key" in str(exc).lower():
            raise HTTPException(
                status_code=409,
                detail="Customer reference already exists"
            )

        raise HTTPException(
            status_code=500,
            detail="Failed to create customer"
        )


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(CUSTOMER_BY_ID, (customer_id,))
            row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {
        "id": row[0],
        "customer_ref": row[1],
        "name": row[2],
        "created_at": row[3].isoformat()
    }


@app.post("/api/payments")
def create_payment(payment: PaymentCreate):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:

                # Make sure the customer exists.
                cursor.execute(
                    CUSTOMER_BY_ID,
                    (payment.customer_id,)
                )

                if cursor.fetchone() is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Customer not found"
                    )

                # Check for an existing transaction reference.
                cursor.execute(
                    """
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
                    WHERE transaction_ref = %s
                    ORDER BY id
                    LIMIT 1;
                    """,
                    (payment.transaction_ref,)
                )

                existing = cursor.fetchone()

                if existing:
                    existing_customer_id = existing[2]
                    existing_amount = existing[3]

                    if (
                        existing_customer_id == payment.customer_id
                        and existing_amount == payment.amount
                    ):
                        connection.rollback()
                        return transaction_to_dict(existing)

                    connection.rollback()
                    raise HTTPException(
                        status_code=409,
                        detail="Transaction reference already exists with different payment details"
                    )

                cursor.execute(
                    CREATE_PAYMENT,
                    (
                        payment.transaction_ref,
                        payment.customer_id,
                        payment.amount
                    )
                )
                row = cursor.fetchone()

                connection.commit()

        return JSONResponse(
            status_code=201,
            content=jsonable_encoder(transaction_to_dict(row))
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to create payment"
        )


@app.get("/api/payments/{payment_id}")
def get_payment(payment_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                TRANSACTION_BY_ID,
                (payment_id,)
            )
            row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return transaction_to_dict(row)


@app.get("/api/customers/{customer_id}/payments")
def get_customer_payments(customer_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                CUSTOMER_BY_ID,
                (customer_id,)
            )

            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="Customer not found"
                )

            cursor.execute(
                CUSTOMER_TRANSACTIONS,
                (customer_id,)
            )

            rows = cursor.fetchall()

    return [transaction_to_dict(row) for row in rows]
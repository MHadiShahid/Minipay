import time

import httpx


BASE_URL = "http://127.0.0.1:8000"


def test_health():
    response = httpx.get(f"{BASE_URL}/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["database"] == "connected"


def test_get_existing_customer():
    response = httpx.get(f"{BASE_URL}/api/customers/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert "customer_ref" in data
    assert "name" in data
    assert "created_at" in data


def test_get_unknown_customer():
    response = httpx.get(f"{BASE_URL}/api/customers/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"


def test_get_unknown_payment():
    response = httpx.get(f"{BASE_URL}/api/payments/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"


def test_create_customer():
    customer_ref = f"API-TEST-{int(time.time())}"

    response = httpx.post(
        f"{BASE_URL}/api/customers",
        json={
            "customer_ref": customer_ref,
            "name": "API Test Customer",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["customer_ref"] == customer_ref
    assert data["name"] == "API Test Customer"
    assert isinstance(data["id"], int)
    assert "created_at" in data


def test_create_payment():
    transaction_ref = f"API-TEST-PAY-{int(time.time())}"

    response = httpx.post(
        f"{BASE_URL}/api/payments",
        json={
            "transaction_ref": transaction_ref,
            "customer_id": 1,
            "amount": 1000.50,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["transaction_ref"] == transaction_ref
    assert data["customer_id"] == 1
    assert float(data["amount"]) == 1000.50
    assert data["status"] == "PROCESSING"
    assert data["completed_at"] is None
    assert data["failure_code"] is None


def test_create_payment_unknown_customer():
    response = httpx.post(
        f"{BASE_URL}/api/payments",
        json={
            "transaction_ref": f"API-UNKNOWN-{int(time.time())}",
            "customer_id": 999999,
            "amount": 1000.00,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Customer not found"


def test_create_payment_invalid_amount():
    response = httpx.post(
        f"{BASE_URL}/api/payments",
        json={
            "transaction_ref": f"API-INVALID-{int(time.time())}",
            "customer_id": 1,
            "amount": -100,
        },
    )

    assert response.status_code == 422


def test_create_payment_missing_field():
    response = httpx.post(
        f"{BASE_URL}/api/payments",
        json={
            "transaction_ref": f"API-MISSING-{int(time.time())}",
            "customer_id": 1,
        },
    )

    assert response.status_code == 422


def test_payment_idempotency():
    transaction_ref = f"API-IDEMPOTENT-{int(time.time())}"

    payload = {
        "transaction_ref": transaction_ref,
        "customer_id": 1,
        "amount": 750.00,
    }

    first_response = httpx.post(
        f"{BASE_URL}/api/payments",
        json=payload,
    )

    assert first_response.status_code == 201

    first_data = first_response.json()

    second_response = httpx.post(
        f"{BASE_URL}/api/payments",
        json=payload,
    )

    assert second_response.status_code == 200

    second_data = second_response.json()

    assert second_data["id"] == first_data["id"]
    assert second_data["transaction_ref"] == first_data["transaction_ref"]
    assert float(second_data["amount"]) == float(first_data["amount"])


def test_payment_conflicting_duplicate():
    transaction_ref = f"API-CONFLICT-{int(time.time())}"

    first_response = httpx.post(
        f"{BASE_URL}/api/payments",
        json={
            "transaction_ref": transaction_ref,
            "customer_id": 1,
            "amount": 500.00,
        },
    )

    assert first_response.status_code == 201

    second_response = httpx.post(
        f"{BASE_URL}/api/payments",
        json={
            "transaction_ref": transaction_ref,
            "customer_id": 1,
            "amount": 600.00,
        },
    )

    assert second_response.status_code == 409
    assert (
        second_response.json()["detail"]
        == "Transaction reference already exists with different payment details"
    )


def test_get_customer_payments():
    response = httpx.get(
        f"{BASE_URL}/api/customers/1/payments"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_payment_response_time():
    start = time.perf_counter()

    response = httpx.get(
        f"{BASE_URL}/api/payments/50006"
    )

    elapsed = time.perf_counter() - start

    assert response.status_code == 200
    assert elapsed < 2.0
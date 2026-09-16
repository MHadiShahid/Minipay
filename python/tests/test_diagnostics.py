from datetime import datetime
from decimal import Decimal

from python.diagnostics import analyze_transaction


def make_transaction(
    status="SUCCESS",
    completed_at=None,
    failure_code=None,
):
    transaction = (
        1,
        "TXN00000001",
        655,
        "CUST000655",
        "Customer 655",
        Decimal("11221.97"),
        status,
        datetime(2026, 9, 9, 23, 59, 32),
        completed_at,
        failure_code,
    )

    callbacks = [
        (
            1,
            200,
            "SUCCESS",
            datetime(2026, 9, 10, 0, 0, 6),
        )
    ]

    return {
        "transaction": transaction,
        "callbacks": callbacks,
    }


def test_successful_transaction_has_no_anomalies():
    data = make_transaction(
        status="SUCCESS",
        completed_at=datetime(2026, 9, 10, 0, 0, 1),
    )

    result = analyze_transaction(data)

    assert result["status"] == "SUCCESS"
    assert result["amount"] == "11221.97"
    assert result["callback_attempts"] == 1
    assert result["successful_callbacks"] == 1
    assert result["failed_callbacks"] == 0
    assert result["anomalies"] == []


def test_failed_transaction_reports_failure_code():
    data = make_transaction(
        status="FAILED",
        completed_at=datetime(2026, 9, 1, 23, 16, 18),
        failure_code="UPSTREAM_ERROR",
    )

    result = analyze_transaction(data)

    assert result["status"] == "FAILED"
    assert result["failure_code"] == "UPSTREAM_ERROR"
    assert any(
        "UPSTREAM_ERROR" in anomaly
        for anomaly in result["anomalies"]
    )


def test_failed_callbacks_are_detected():
    data = make_transaction(
        status="FAILED",
        completed_at=datetime(2026, 9, 1, 23, 16, 18),
        failure_code="UPSTREAM_ERROR",
    )

    data["callbacks"] = [
        (
            1,
            502,
            "FAILED",
            datetime(2026, 9, 1, 23, 16, 23),
        )
    ]

    result = analyze_transaction(data)

    assert result["callback_attempts"] == 1
    assert result["failed_callbacks"] == 1
    assert result["successful_callbacks"] == 0
    assert result["callback_details"][0]["http_status"] == 502
    assert any(
        "All recorded callback attempts failed" in anomaly
        for anomaly in result["anomalies"]
    )


def test_processing_transaction_without_callbacks_is_detected():
    data = make_transaction(
        status="PROCESSING",
        completed_at=None,
        failure_code=None,
    )

    data["callbacks"] = []

    result = analyze_transaction(data)

    assert result["status"] == "PROCESSING"
    assert result["callback_attempts"] == 0
    assert "Transaction is still PROCESSING." in result["anomalies"]
    assert "No callback attempts were recorded." in result["anomalies"]


def test_successful_transaction_without_callback_is_anomalous():
    data = make_transaction(
        status="SUCCESS",
        completed_at=datetime(2026, 9, 10, 0, 0, 1),
    )

    data["callbacks"] = []

    result = analyze_transaction(data)

    assert "No callback attempts were recorded." in result["anomalies"]
    assert "successful transaction has no callback" in (
        result["recommended_next_action"]
    )


def test_duplicate_transaction_reference_is_detected():
    data = make_transaction(
        status="SUCCESS",
        completed_at=datetime(2026, 9, 10, 0, 0, 1),
    )

    result = analyze_transaction(
        data,
        duplicate_count=2,
    )

    assert result["duplicate_reference"] is True
    assert result["duplicate_count"] == 2
    assert any(
        "duplicated across 2 transaction records" in anomaly
        for anomaly in result["anomalies"]
    )


def test_callback_retry_details_are_preserved():
    data = make_transaction(
        status="SUCCESS",
        completed_at=datetime(2026, 9, 10, 0, 0, 1),
    )

    data["callbacks"] = [
        (
            1,
            502,
            "FAILED",
            datetime(2026, 9, 10, 0, 0, 6),
        ),
        (
            2,
            200,
            "SUCCESS",
            datetime(2026, 9, 10, 0, 0, 12),
        ),
    ]

    result = analyze_transaction(data)

    assert result["callback_attempts"] == 2
    assert result["failed_callbacks"] == 1
    assert result["successful_callbacks"] == 1
    assert result["callback_details"][0]["attempt_no"] == 1
    assert result["callback_details"][0]["http_status"] == 502
    assert result["callback_details"][1]["attempt_no"] == 2
    assert result["callback_details"][1]["http_status"] == 200
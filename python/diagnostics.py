from datetime import datetime


def format_datetime(value):
    if isinstance(value, datetime):
        return value.isoformat()

    if value is None:
        return None

    return str(value)


def analyze_transaction(data, duplicate_count=1):
    transaction = data["transaction"]
    callbacks = data["callbacks"]

    (
        transaction_id,
        transaction_ref,
        customer_id,
        customer_ref,
        customer_name,
        amount,
        status,
        created_at,
        completed_at,
        failure_code,
    ) = transaction

    callback_attempts = len(callbacks)
    successful_callbacks = sum(
        1 for callback in callbacks if callback[2] == "SUCCESS"
    )
    failed_callbacks = sum(
        1 for callback in callbacks if callback[2] == "FAILED"
    )

    last_callback_at = (
        callbacks[-1][3]
        if callbacks
        else None
    )

    anomalies = []
    next_action = "No immediate action required."

    if duplicate_count > 1:
        anomalies.append(
            f"Transaction reference is duplicated across "
            f"{duplicate_count} transaction records."
        )
        next_action = (
            "Investigate duplicate transaction references and "
            "confirm which transaction record is authoritative."
        )

    if status == "PROCESSING":
        anomalies.append("Transaction is still PROCESSING.")
        next_action = (
            "Check payment processing logs and downstream "
            "processing status."
        )

    if status == "FAILED":
        if failure_code:
            anomalies.append(
                f"Transaction failed with code {failure_code}."
            )
        else:
            anomalies.append(
                "Transaction is FAILED without a failure code."
            )

        next_action = (
            "Investigate the failure code and related "
            "application logs."
        )

    if callback_attempts == 0:
        anomalies.append("No callback attempts were recorded.")

        if status == "SUCCESS":
            next_action = (
                "Investigate why the successful transaction "
                "has no callback attempt."
            )
        elif status == "FAILED":
            next_action = (
                "Check whether callback processing was skipped "
                "and review the transaction failure logs."
            )

    elif failed_callbacks > 0 and successful_callbacks == 0:
        anomalies.append("All recorded callback attempts failed.")
        next_action = (
            "Check callback endpoint availability and "
            "retry processing."
        )

    elif failed_callbacks > 0:
        anomalies.append(
            "One or more callback attempts failed before "
            "a successful callback."
        )

    if status == "SUCCESS" and completed_at is None:
        anomalies.append(
            "Transaction is SUCCESS but has no completed_at timestamp."
        )
        next_action = (
            "Check transaction completion handling "
            "and data consistency."
        )

    callback_details = []

    for callback in callbacks:
        attempt_no, http_status, callback_status, attempted_at = callback

        callback_details.append(
            {
                "attempt_no": attempt_no,
                "http_status": http_status,
                "callback_status": callback_status,
                "attempted_at": format_datetime(attempted_at),
            }
        )

    return {
        "transaction_id": transaction_id,
        "transaction_ref": transaction_ref,
        "customer_id": customer_id,
        "customer_ref": customer_ref,
        "customer_name": customer_name,
        "amount": str(amount),
        "status": status,
        "created_at": format_datetime(created_at),
        "completed_at": format_datetime(completed_at),
        "failure_code": failure_code,
        "callback_attempts": callback_attempts,
        "successful_callbacks": successful_callbacks,
        "failed_callbacks": failed_callbacks,
        "last_callback_at": format_datetime(last_callback_at),
        "callback_details": callback_details,
        "duplicate_reference": duplicate_count > 1,
        "duplicate_count": duplicate_count,
        "anomalies": anomalies,
        "recommended_next_action": next_action,
    }
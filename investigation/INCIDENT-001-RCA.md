# INCIDENT-001 RCA — Intermittent Transaction Lookup HTTP 500

## Incident Summary

* **Incident:** INCIDENT-001
* **Priority:** P2
* **Reported symptom:** Transaction searches intermittently return HTTP 500. Some transaction IDs work while others fail.
* **Affected workflow:** MiniPay support-console payment lookup through `GET /api/payments/{payment_id}`.
* **Investigation date:** 2026-09-17

The current MiniPay API does not expose a transaction-reference search endpoint. The implemented support-console lookup uses payment ID lookup, so the incident was reproduced against that existing workflow rather than inventing an unavailable endpoint.

## Baseline Observations

Before introducing the controlled defect:

```text
GET /api/payments/1
HTTP/1.1 200 OK
```

Transaction 1:

```text
id=1
transaction_ref=TXN00000001
status=SUCCESS
```

A nonexistent payment correctly returned:

```text
GET /api/payments/999999
HTTP/1.1 404 Not Found
{"detail":"Payment not found"}
```

The database contains multiple transaction states:

```text
1   TXN00000001   SUCCESS
10  TXN00000010   FAILED
29  TXN00000029   PROCESSING
```

## Reproduction

The assessment permits controlled defect injection when the existing implementation does not naturally reproduce the incident. A temporary application-layer regression was therefore introduced and explicitly removed after reproduction.

The temporary defect was:

```python
if row[4] == 'SUCCESS':
    _ = row[8]
```

The transaction query returns eight fields, indexed `0` through `7`. Accessing `row[8]` therefore raises an `IndexError`, but only for transactions whose status is `SUCCESS`.

### Reproduction Results

| Payment ID | Status     | Result   |
| ---------: | ---------- | -------- |
|          1 | SUCCESS    | HTTP 500 |
|         10 | FAILED     | HTTP 200 |
|         29 | PROCESSING | HTTP 200 |

Successful transaction during reproduction:

```text
GET /api/payments/1
HTTP/1.1 500 Internal Server Error
```

Failed transaction during reproduction:

```text
GET /api/payments/10
HTTP/1.1 200 OK
```

Processing transaction during reproduction:

```text
GET /api/payments/29
HTTP/1.1 200 OK
```

This reproduced the intermittent behavior: the result depended on the transaction's data state rather than all lookups failing.

## Evidence

The transaction mapping uses positional database fields:

```python
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
```

The controlled regression attempted to access index `8`, which does not exist.

The underlying SQL query was verified and remained unchanged:

```sql
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
```

The query returns exactly eight columns.

## Root Cause

### Controlled reproduction root cause

A response-mapping regression attempted to access a ninth field from an eight-column database result for `SUCCESS` transactions.

Because the invalid access was conditional on:

```python
row[4] == 'SUCCESS'
```

successful transactions produced HTTP 500 while `FAILED` and `PROCESSING` transactions continued to return successfully.

This defect was deliberately injected solely to reproduce the assessment's intermittent-500 scenario because the original implementation did not naturally contain this failure.

## Immediate Corrective Action

The temporary defective code was removed by restoring the backed-up `api/app/main.py`.

Validation after restoration:

```text
GET /api/payments/1
HTTP/1.1 200 OK
```

Response:

```json
{
  "id": 1,
  "transaction_ref": "TXN00000001",
  "customer_id": 655,
  "amount": 11221.97,
  "status": "SUCCESS",
  "created_at": "2026-09-09T23:59:32",
  "completed_at": "2026-09-10T00:00:01",
  "failure_code": null
}
```

The temporary backup files were deleted after restoration.

## Permanent Corrective / Preventive Actions

1. Keep database result mappings aligned with the selected columns.
2. Prefer named-row/database-record access where practical to reduce positional-index mistakes.
3. Add automated API tests covering `SUCCESS`, `FAILED`, and `PROCESSING` transaction states.
4. Add a regression test verifying that successful payment lookup returns HTTP 200 and all expected response fields.
5. Monitor API logs for unexpected HTTP 5xx responses and correlate them with endpoint and transaction state.
6. Treat query changes and response-mapping changes as a single change set so that selected fields and application indexes remain synchronized.

## Validation

After removing the controlled defect:

```text
GET /api/payments/1
HTTP/1.1 200 OK
```

The application returned to its original healthy behavior.

## Notes

This RCA documents a **controlled defect injection**, as explicitly permitted by the assessment instructions. The HTTP 500 is not claimed to have been an organically occurring defect in the original implementation.

The investigation demonstrates the L2 troubleshooting workflow:

1. Establish a healthy baseline.
2. Reproduce the intermittent failure.
3. Compare successful and failing transaction states.
4. Isolate the data-dependent application failure.
5. Identify the faulty response mapping.
6. Remove the defect.
7. Validate recovery.

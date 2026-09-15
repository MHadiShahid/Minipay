# API Test Notes

## Test Framework

The API tests use `pytest` with `httpx` to send HTTP requests to the running MiniPay API.

## Running the Tests

Start the FastAPI application first, then run the complete API test suite from the project root:

```cmd
pytest tests\api\test_api.py -v

The tests target:

http://127.0.0.1:8000
Test Coverage

The automated tests cover:

Health check and database connectivity
Existing customer retrieval
Unknown customer handling
Unknown payment handling
Customer creation
Payment creation
Unknown customer validation during payment creation
Invalid payment amount
Missing required fields
Idempotent payment replay
Conflicting duplicate payment reference
Customer payment history
Basic API response-time validation
HTTP Status Codes

The tests distinguish between client-side and server-side errors:

200 OK - Successful retrieval or idempotent replay
201 Created - New customer or payment successfully created
404 Not Found - Requested customer or payment does not exist
409 Conflict - Existing transaction reference conflicts with the supplied payment details
422 Unprocessable Content - Request validation failed
500 Internal Server Error - Unexpected server-side failure
Timeouts and Retries

The current tests use httpx requests without automatic retries.

Retries are intentionally not enabled in the test client because automatic retries can hide real API failures and make test results less deterministic.

The response-time test uses a two-second threshold for a simple payment retrieval request.

For production integrations, connection and read timeouts should be configured explicitly and retry behavior should be limited to operations that are safe to retry.

Idempotency

Payment creation uses transaction_ref as the idempotency reference.

When the same transaction reference is submitted with the same customer and amount, the existing transaction is returned instead of creating another transaction.

A request using an existing transaction reference with different payment details returns 409 Conflict.

This prevents accidental duplicate creation during client retries while detecting conflicting reuse of a transaction reference.

4xx vs 5xx

4xx responses represent invalid requests or client-side conditions, such as:

Missing or invalid fields
Unknown resources
Conflicting payment details

5xx responses represent unexpected server-side failures.

The automated tests verify expected 4xx behavior. Unexpected 5xx responses cause the relevant tests to fail.
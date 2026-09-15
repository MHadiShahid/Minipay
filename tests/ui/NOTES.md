\# UI Automation Notes



\## Framework



The UI tests use Playwright with Chromium.



\## Running the Tests



Start the FastAPI backend and frontend server first.



From the project root:



```cmd

npm run test:ui



The frontend is expected at:



http://127.0.0.1:5500



The API is expected at:



http://127.0.0.1:8000

Test Coverage



The Playwright smoke/regression suite covers:



Support console page loading

API health status

Existing customer lookup

Unknown customer error handling

Payment creation

Existing payment lookup

Unknown payment error handling

Customer payment history

Selectors



The frontend uses data-testid attributes for important interactive elements and result containers.



This avoids depending on styling classes or fragile DOM structure.



Examples include:



customer-id

customer-search

customer-result

transaction-ref

create-payment

payment-id

payment-search

payment-lookup-result

payments-customer-id

payments-search

payments-result

Test Data



The payment creation test generates a unique transaction reference using the current timestamp. This prevents repeated test runs from conflicting with previous test data.



Existing seeded records are used for read-only lookup tests.



Failure Evidence



Playwright is configured to:



Capture screenshots when a test fails

Retain traces when a test fails

Generate an HTML test report



The latest report can be opened with:



npx playwright show-report


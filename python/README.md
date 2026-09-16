\# Python Support Tool



\## Purpose



`support\_tool.py` is a transaction diagnostic CLI for MiniPay support and L2 troubleshooting.



It retrieves transaction, customer, and callback information from PostgreSQL and reports detected anomalies and recommended next actions.



\## Requirements



\- Python 3.13+

\- PostgreSQL

\- `psycopg`



Install the Python dependency with:



```cmd

pip install -r python\\requirements.txt

Configuration



The tool uses environment variables instead of hard-coded credentials.



Required:



DATABASE\_URL



Optional:



API\_URL

DB\_TIMEOUT

API\_TIMEOUT



Example:



set DATABASE\_URL=postgresql://minipay:minipay123@127.0.0.1:5432/minipay

set API\_URL=http://127.0.0.1:8000

set DB\_TIMEOUT=5

set API\_TIMEOUT=5

Transaction Diagnostic



Minimum required usage:



python python\\support\_tool.py --transaction TXN00000001



The report includes:



Transaction ID and reference

Customer ID, reference, and name

Amount

Transaction status

Created and completed timestamps

Failure code

Callback attempt count

Successful and failed callback counts

Callback HTTP status

Callback attempt timestamps

Detected anomalies

Recommended next action

JSON Output



For machine-readable output:



python python\\support\_tool.py --transaction TXN00000001 --json

Health Check



The tool also provides an API and database health check:



python python\\support\_tool.py --health



Machine-readable health output:



python python\\support\_tool.py --health --json

Exit Codes

Code	Meaning

0	Successful diagnostic or healthy checks

1	Configuration, database, API, or other operational error

2	Transaction reference was not found

Error and Timeout Handling



Database connections use a configurable connection timeout through DB\_TIMEOUT.



API health checks use the configurable API\_TIMEOUT.



Database/API failures are logged and returned as errors rather than causing an unhandled traceback.



Logging



The tool logs diagnostic activity and operational failures.



Logs are written separately from JSON output so that --json remains machine-readable.



Unit Tests



Diagnostic logic is tested independently of the database.



Run:



pytest python\\tests\\test\_diagnostics.py -v



The tests cover:



Successful transactions

Failed transactions

Failure codes

Failed callbacks

Processing transactions

Missing callbacks

Duplicate transaction references

Callback retry details

Example



For a failed transaction:



Status:               FAILED

Failure Code:         UPSTREAM\_ERROR



Callback / Retry Details:

\- Attempt 1: HTTP 502 | FAILED | ...



Anomalies:

\- Transaction failed with code UPSTREAM\_ERROR.

\- All recorded callback attempts failed.



Recommended Next Action:

Check callback endpoint availability and retry processing.


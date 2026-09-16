\# INCIDENT-003 RCA — Slow Transaction Investigation



\## Incident Summary



\* \*\*Incident:\*\* INCIDENT-003

\* \*\*Priority:\*\* P2

\* \*\*Reported symptom:\*\* Transaction investigation becomes slower as transaction volume increases.

\* \*\*Affected area:\*\* Transaction lookup by `transaction\_ref`.

\* \*\*Investigation date:\*\* 2026-09-17



\## Observations



The MiniPay PostgreSQL database contains approximately 50,000 transactions.



The transaction table initially did not have an index on `transaction\_ref`.



The investigation query was:



```sql

EXPLAIN (ANALYZE, BUFFERS)

SELECT

&#x20;   id,

&#x20;   transaction\_ref,

&#x20;   customer\_id,

&#x20;   amount,

&#x20;   status,

&#x20;   created\_at,

&#x20;   completed\_at,

&#x20;   failure\_code

FROM transactions

WHERE transaction\_ref = 'TXN00012345';

```



The query searches for a single transaction reference, but without an index PostgreSQL must scan the transaction table.



\## Baseline Evidence



Before optimization, PostgreSQL produced a sequential scan.



Key observations:



```text

Scan type: Sequential Scan

Rows Removed by Filter: 49,999

Buffers: 616

Execution Time: 10.225 ms

```



The sequential scan means PostgreSQL examined the table rather than directly locating the requested transaction.



As transaction volume increases, this access pattern requires progressively more rows to be examined.



\## Root Cause



The transaction investigation query filtered on `transaction\_ref`, but the column did not have an appropriate index.



The resulting sequential scan caused unnecessary table reads and made transaction investigation less efficient as the dataset grew.



\## Corrective Action



An index was created on `transaction\_ref`:



```sql

CREATE INDEX idx\_transactions\_transaction\_ref

ON transactions(transaction\_ref);

```



The index was intentionally created as a non-unique index because the existing schema permits duplicate transaction references and the investigation did not establish that `transaction\_ref` is a unique business key.



\## Post-Optimization Evidence



The same `EXPLAIN (ANALYZE, BUFFERS)` query was executed after creating the index.



Post-optimization results:



```text

Scan type: Index Scan

Buffers: 3 (hit=1 read=2)

Execution Time: 0.102 ms

```



The query changed from a sequential scan to an index scan.



\## Before / After



| Metric                 |          Before |                          After |

| ---------------------- | --------------: | -----------------------------: |

| Access method          | Sequential Scan |                     Index Scan |

| Rows removed by filter |          49,999 | Not applicable to index lookup |

| Buffers                |             616 |                              3 |

| Execution time         |       10.225 ms |                       0.102 ms |



The measured execution time improved by approximately two orders of magnitude for the tested query.



\## Validation



The same transaction-reference lookup was executed with `EXPLAIN (ANALYZE, BUFFERS)` before and after the index was created.



The post-optimization plan confirmed that PostgreSQL used the new `idx\_transactions\_transaction\_ref` index.



The optimization therefore addressed the identified access-pattern bottleneck.



\## Preventive Actions



1\. Review frequently used transaction-investigation filters when designing database indexes.

2\. Use `EXPLAIN (ANALYZE, BUFFERS)` when investigating slow SQL rather than relying only on application response time.

3\. Monitor query performance as transaction volume grows.

4\. Review new support and investigation queries for appropriate indexing.

5\. Avoid adding indexes blindly; validate them against actual query patterns and workload.



\## Evidence Reference



Detailed SQL investigation and performance measurements are documented in:



```text

sql/PERFORMANCE.md

```



The corresponding SQL investigation scripts are under:



```text

sql/

```




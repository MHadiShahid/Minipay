# SQL Performance Investigation

## Problem

Transaction search by `transaction_ref` was identified as a potentially inefficient access pattern.

The `transactions` table contains 50,000 rows, and `transaction_ref` was not indexed in the supplied schema.

## Baseline

Query tested:

```sql
EXPLAIN (ANALYZE, BUFFERS)
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
WHERE transaction_ref = 'TXN00012345';
Before Index

The query used a sequential scan:

Seq Scan on transactions
Rows Removed by Filter: 49999
Buffers: shared hit=616
Execution Time: 10.225 ms

The database scanned the entire transactions table even though only one matching transaction was required.

Improvement:

An index was created on transaction_ref:

CREATE INDEX idx_transactions_transaction_ref
ON transactions(transaction_ref);

The index is intentionally non-unique because the supplied schema allows duplicate transaction references.

After Index:

The same query was executed again.

Index Scan using idx_transactions_transaction_ref on transactions
Buffers: shared hit=1 read=2
Execution Time: 0.102 ms
Before vs After
Metric	                      Before	                After
Access method	              Sequential Scan	        Index Scan
Rows removed by filter	      49,999	                0
Buffers	                      616	                3
Execution time	              10.225 ms           	0.102 ms

The measured execution time decreased from 10.225 ms to 0.102 ms, approximately a 100x improvement for this test query.

Conclusion:

Searching transactions by transaction_ref without an index requires scanning the full table. Adding an index allows PostgreSQL to locate matching transaction records directly.This index is appropriate for transaction-search workloads because transaction_ref is used as a lookup field. The index is not declared UNIQUE because duplicate transaction references are present in the supplied assessment data.
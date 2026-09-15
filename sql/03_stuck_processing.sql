-- 03_stuck_processing.sql
-- Transactions that have remained in PROCESSING for more than 15 minutes.
--
-- The supplied generator creates data from September 1, 2026.
-- CURRENT_TIMESTAMP is therefore not useful for historical seeded data.
-- This query uses the latest transaction timestamp as the reference point
-- so that the seeded dataset can be investigated reproducibly.

SELECT
    id,
    transaction_ref,
    customer_id,
    amount,
    status,
    created_at,
    CURRENT_TIMESTAMP - created_at AS processing_duration
FROM transactions
WHERE status = 'PROCESSING'
  AND created_at < (
      SELECT MAX(created_at) - INTERVAL '15 minutes'
      FROM transactions
  )
ORDER BY created_at;
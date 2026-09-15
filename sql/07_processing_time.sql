-- 07_processing_time.sql
-- Average and p95 processing time for transactions with completion timestamps.
-- Processing time is measured from created_at to completed_at.

SELECT
    ROUND(
        AVG(EXTRACT(EPOCH FROM (completed_at - created_at)))::numeric,
        2
    ) AS average_processing_seconds,
    ROUND(
        PERCENTILE_CONT(0.95) WITHIN GROUP (
            ORDER BY EXTRACT(EPOCH FROM (completed_at - created_at))
        )::numeric,
        2
    ) AS p95_processing_seconds
FROM transactions
WHERE completed_at IS NOT NULL;

-- 04_duplicate_refs.sql
-- Transaction references that occur more than once.

SELECT
    transaction_ref,
    COUNT(*) AS occurrence_count
FROM transactions
GROUP BY transaction_ref
HAVING COUNT(*) > 1
ORDER BY occurrence_count DESC, transaction_ref;
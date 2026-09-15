-- 06_reconciliation.sql
-- Reconcile successful transactions against transactions whose callback
-- ultimately succeeded.
--
-- A transaction can have multiple callback attempts, so each transaction
-- is counted at most once in the callback-success side.

WITH successful_transactions AS (
    SELECT
        id,
        amount
    FROM transactions
    WHERE status = 'SUCCESS'
),
callback_success AS (
    SELECT DISTINCT
        transaction_id
    FROM callbacks
    WHERE callback_status = 'SUCCESS'
)
SELECT
    COUNT(st.id) AS successful_transaction_count,
    COALESCE(SUM(st.amount), 0) AS successful_transaction_value,
    COUNT(cs.transaction_id) AS callback_success_count,
    COALESCE(SUM(st.amount) FILTER (
        WHERE cs.transaction_id IS NOT NULL
    ), 0) AS callback_success_value,
    COUNT(st.id) - COUNT(cs.transaction_id) AS count_difference,
    COALESCE(SUM(st.amount), 0)
        - COALESCE(SUM(st.amount) FILTER (
            WHERE cs.transaction_id IS NOT NULL
        ), 0) AS value_difference
FROM successful_transactions st
LEFT JOIN callback_success cs
    ON cs.transaction_id = st.id;
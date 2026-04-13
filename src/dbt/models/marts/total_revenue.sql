WITH events AS (
    SELECT * FROM {{ ref('stg_events') }}
)

SELECT
    DATE(event_at) AS date,
    status,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_revenue
FROM events
GROUP BY 1, 2
ORDER BY 1 DESC

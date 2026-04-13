WITH source AS (
    SELECT * FROM {{ source('public', 'landing_events') }}
),

renamed AS (
    SELECT
        id AS event_id,
        user_id,
        amount,
        status,
        timestamp AS event_at
    FROM source
)

SELECT * FROM renamed

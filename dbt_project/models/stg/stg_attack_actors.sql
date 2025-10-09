select

    eventid AS event_id
    , COALESCE(NULLIF(gname, 'Unknown'), 'Unspecified') AS primary_group
    , NULLIF(gsubname, '') AS subgroup
    , NULLIF(gname2, '') AS secondary_group
    , NULLIF(gname3, '') AS tertiary_group

from {{ ref('raw', 'raw_gtd')}}
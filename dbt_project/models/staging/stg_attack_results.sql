select

    eventid as event_id
    , nkill::float::int AS num_killed
    , nperps::float::int as num_perpetrators
    , nwound::float::int AS num_wounded
    , property::float::int as num_properties_damaged
    , (success = 1) AS was_successful
    , (suicide = 1) AS had_suicide
    , CASE
        WHEN approxdate IS NOT NULL AND approxdate ~ '\d{2}/\d{2}/\d{4}'
        THEN TO_DATE(approxdate, 'MM/DD/YYYY')
        ELSE NULL
    End as approx_date
    , iyear as year
    , motive
    , summary

from {{ref('raw_gtd')}}
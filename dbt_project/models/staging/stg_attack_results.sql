select

    eventid as event_id
    , nkill::int AS num_killed
    , nperps::int as num_perpetrators
    , nwound::int AS num_wounded
    , property::int as num_properties_damaged
    , (success = 1) AS was_successful
    , (suicide = 1) AS had_suicide
    , CASE
    WHEN approxdate is not null and approxdate ~ '\d{4}' then
        to_date(
            regexp_replace(approxdate, '(\d+)-\d+', '\1')
            , 'Month DD, YYYY'
        )
    ELSE NULL
    End as approx_date
    , iyear as year
    , motive
    , summary

from {{ref('raw_gtd')}}
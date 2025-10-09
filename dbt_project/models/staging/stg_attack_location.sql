select

    eventid as event_id
    , country as country_id
    , country_txt as country
    , region as region_id
    , region_txt as region
    , provstate as province_state
    , city
    , latitude::float
    , longitude::float
    , specificity
    , vicinity
    , location

from {{ref('raw_gtd')}}
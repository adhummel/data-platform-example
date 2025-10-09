select

    eventid as event_id
    , targtype1_txt AS target_category
    , targsubtype1_txt AS target_subcategory
    , corp1 AS target_corporation
    , target1 AS target_name
    , natlty1_txt AS target_nationality

from {{ref('raw', 'raw_gtd')}}
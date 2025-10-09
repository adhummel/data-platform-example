select

    eventid as event_id
    , 
    , weaptype1_txt AS weapon_type_id
    , weapsubtype1_txt AS weapon_type
    , weapdetail AS weapon_description

from {{ref('raw', 'raw_gtd')}}
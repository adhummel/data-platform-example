-- models/marts/mart_group_expansion.sql
-- Answer: "Which groups are expanding fastest?"

select
    primary_group,
    countries_operated,
    countries_per_year as expansion_velocity,
    new_countries_last_5yrs as recent_expansion,
    years_active,
    primary_base_country,
    expansion_rate,
    threat_classification,
    
    -- Rank by expansion speed
    row_number() over (order by countries_per_year desc, new_countries_last_5yrs desc) 
        as expansion_rank
        
from {{ ref('int_group_expansion_tracking') }}
where expansion_rate in ('Rapid Expansion', 'Steady Expansion')
order by expansion_velocity desc
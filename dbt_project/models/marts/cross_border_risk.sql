-- models/marts/mart_cross_border_risk.sql
-- Answer: "Which countries face cross-border spillover?"

select
    target_country,
    count(distinct source_country) as num_source_countries,
    sum(total_spillover_attacks) as total_spillover_attacks,
    sum(num_shared_groups) as total_shared_groups,
    avg(avg_expansion_lag_years) as avg_time_to_spillover_years,
    sum(spillover_intensity_score) as total_spillover_risk_score,
    
    -- Top sources
    (array_agg(source_country order by spillover_intensity_score desc))[1:3] 
        as top_source_countries
        
from {{ ref('int_cross_border_flows') }}
group by target_country
having sum(total_spillover_attacks) > 10
order by total_spillover_risk_score desc
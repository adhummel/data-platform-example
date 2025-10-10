-- models/marts/mart_group_clustering_features.sql
-- Answer: "Which groups have similar behavior patterns?"

select
    primary_group,
    behavioral_archetype,
    
    -- Feature vector for clustering
    normalized_attack_volume,
    normalized_lethality,
    normalized_geographic_reach,
    suicide_attack_rate_pct,
    success_rate_pct,
    explosives_pct,
    firearms_pct,
    govt_target_pct,
    civilian_target_pct,
    
    -- Context
    total_attacks,
    countries_operated
    
from {{ ref('int_group_behavioral_signatures') }}
order by total_attacks desc
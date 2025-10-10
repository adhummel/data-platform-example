-- models/intermediate/int_group_behavioral_signatures.sql
-- Behavioral features for group clustering and similarity analysis

{{
  config(
    materialized='table',
    schema='intermediate'
  )
}}

with group_attack_features as (
    select
        primary_group,
        
        -- Operational characteristics
        count(*) as total_attacks,
        sum(total_casualties) as total_casualties,
        avg(total_casualties) as avg_casualties_per_attack,
        stddev(total_casualties) as casualties_stddev,
        
        -- Tactical preferences (% of attacks)
        round(100.0 * sum(case when had_suicide then 1 else 0 end) / count(*), 2) 
            as suicide_attack_rate_pct,
        round(100.0 * sum(case when was_successful then 1 else 0 end) / count(*), 2) 
            as success_rate_pct,
        round(100.0 * sum(case when is_high_impact then 1 else 0 end) / count(*), 2) 
            as high_impact_rate_pct,
        
        -- Weapon preferences (distribution)
        round(100.0 * sum(case when weapon_category = 'Explosives' then 1 else 0 end) / count(*), 2) 
            as explosives_pct,
        round(100.0 * sum(case when weapon_category = 'Firearms' then 1 else 0 end) / count(*), 2) 
            as firearms_pct,
        round(100.0 * sum(case when weapon_category = 'Fire/Incendiary' then 1 else 0 end) / count(*), 2) 
            as incendiary_pct,
        
        -- Target preferences (distribution)
        round(100.0 * sum(case when target_type_simplified = 'Government/Law Enforcement' then 1 else 0 end) / count(*), 2) 
            as govt_target_pct,
        round(100.0 * sum(case when target_type_simplified = 'Military/Armed Groups' then 1 else 0 end) / count(*), 2) 
            as military_target_pct,
        round(100.0 * sum(case when target_type_simplified = 'Civilians' then 1 else 0 end) / count(*), 2) 
            as civilian_target_pct,
        round(100.0 * sum(case when target_type_simplified = 'Infrastructure/Business' then 1 else 0 end) / count(*), 2) 
            as infrastructure_target_pct,
        
        -- Geographic diversity
        count(distinct country) as countries_operated,
        count(distinct region) as regions_operated,
        
        -- Temporal patterns
        max(year) - min(year) + 1 as years_active,
        count(*) / nullif(max(year) - min(year) + 1, 0) as attacks_per_year,
        
        -- Lethality metrics
        max(total_casualties) as max_casualties_single_attack,
        percentile_cont(0.5) within group (order by total_casualties) as median_casualties,
        
        -- Coordination complexity (proxy)
        avg(num_perpetrators) as avg_perpetrators_per_attack
        
    from {{ ref('int_gtd_enriched') }}
    where primary_group != 'Unspecified'
    group by primary_group
    having count(*) >= 20  -- Minimum attack threshold for reliable patterns
),

normalized_features as (
    select
        *,
        
        -- Normalize features for clustering (0-100 scale)
        (total_attacks - min(total_attacks) over()) / 
            nullif(max(total_attacks) over() - min(total_attacks) over(), 0) * 100 
            as normalized_attack_volume,
        
        (avg_casualties_per_attack - min(avg_casualties_per_attack) over()) / 
            nullif(max(avg_casualties_per_attack) over() - min(avg_casualties_per_attack) over(), 0) * 100 
            as normalized_lethality,
        
        (countries_operated - min(countries_operated) over()) / 
            nullif(max(countries_operated) over() - min(countries_operated) over(), 0) * 100 
            as normalized_geographic_reach,
        
        -- Behavioral archetype (simple classification)
        case
            when suicide_attack_rate_pct > 20 and civilian_target_pct > 50 
                then 'Indiscriminate High-Casualty'
            when military_target_pct > 60 
                then 'Military-Focused Insurgent'
            when govt_target_pct > 50 and success_rate_pct > 70 
                then 'State-Targeting Professional'
            when explosives_pct > 70 
                then 'Bombing-Specialized'
            when countries_operated > 5 
                then 'Transnational Network'
            else 'Regional Insurgent'
        end as behavioral_archetype
        
    from group_attack_features
)

select * from normalized_features
order by total_attacks desc
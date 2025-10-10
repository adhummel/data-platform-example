-- models/intermediate/int_group_expansion_tracking.sql
-- Track geographic expansion of terrorist groups over time

{{
  config(
    materialized='table',
    schema='intermediate'
  )
}}

with group_country_timeline as (
    select
        primary_group,
        country,
        min(year) as first_attack_year,
        max(year) as last_attack_year,
        count(*) as total_attacks,
        sum(total_casualties) as total_casualties
    from {{ ref('int_gtd_enriched') }}
    where primary_group != 'Unspecified'
    group by primary_group, country
),

group_metrics as (
    select
        primary_group,
        
        -- Geographic reach
        count(distinct country) as countries_operated,
        min(first_attack_year) as group_origin_year,
        max(last_attack_year) as last_active_year,
        max(last_attack_year) - min(first_attack_year) + 1 as years_active,
        
        -- Expansion velocity
        count(distinct country) / nullif(max(last_attack_year) - min(first_attack_year) + 1, 0) 
            as countries_per_year,
        
        -- Totals
        sum(total_attacks) as total_attacks_all_countries,
        sum(total_casualties) as total_casualties_all_countries,
        
        -- Primary base
        (array_agg(country order by total_attacks desc))[1] as primary_base_country,
        max(total_attacks) as attacks_in_primary_base
        
    from group_country_timeline
    group by primary_group
),

expansion_phases as (
    select
        g.primary_group,
        g.countries_operated,
        g.countries_per_year,
        g.years_active,
        g.primary_base_country,
        
        -- Recent expansion (last 5 years)
        (select count(distinct country) 
         from group_country_timeline t
         where t.primary_group = g.primary_group
         and t.first_attack_year >= g.last_active_year - 5
        ) as new_countries_last_5yrs,
        
        -- Classification
        case
            when g.countries_per_year > 1 then 'Rapid Expansion'
            when g.countries_per_year > 0.5 then 'Steady Expansion'
            when g.countries_per_year > 0 then 'Slow Expansion'
            else 'Contained'
        end as expansion_rate,
        
        -- Threat level
        case
            when g.countries_operated > 10 and g.countries_per_year > 0.5 
                then 'Transnational Threat'
            when g.countries_operated > 5 
                then 'Regional Threat'
            else 'Local Threat'
        end as threat_classification
        
    from group_metrics g
    where g.total_attacks_all_countries >= 50  -- Significant groups only
)

select * from expansion_phases
order by countries_per_year desc, new_countries_last_5yrs desc
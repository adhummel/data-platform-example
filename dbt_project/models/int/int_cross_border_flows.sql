-- models/intermediate/int_cross_border_flows.sql
-- Cross-border terrorism flows and spillover patterns

{{
  config(
    materialized='table',
    schema='intermediate'
  )
}}

with group_operations as (
    select
        primary_group,
        country as target_country,
        region as target_region,
        year,
        count(*) as attacks_in_country,
        sum(total_casualties) as casualties_in_country,
        
        -- First and last attack in this country
        min(year) as first_attack_year,
        max(year) as last_attack_year
    from {{ ref('int_gtd_enriched') }}
    where primary_group is not null 
      and primary_group != 'Unspecified'
    group by primary_group, country, region, year
),

group_country_presence as (
    select
        primary_group,
        count(distinct target_country) as num_countries_operated,
        count(distinct target_region) as num_regions_operated,
        array_agg(distinct target_country order by target_country) as countries_list,
        
        -- Primary base (country with most attacks)
        mode() within group (order by target_country) as primary_base_country,
        max(attacks_in_country) as attacks_in_primary_base
    from group_operations
    group by primary_group
),

cross_border_pairs as (
    select
        g1.primary_group,
        g1.target_country as source_country,
        g2.target_country as target_country,
        g1.year,
        
        -- Spillover metrics
        g1.attacks_in_country as attacks_from_source,
        g2.attacks_in_country as attacks_in_target,
        
        -- Temporal relationship
        g2.year - g1.first_attack_year as years_since_group_origin,
        g2.first_attack_year - g1.first_attack_year as expansion_lag_years
        
    from group_operations g1
    inner join group_operations g2
        on g1.primary_group = g2.primary_group
        and g1.target_country != g2.target_country
        and g2.first_attack_year >= g1.first_attack_year
),

spillover_intensity as (
    select
        source_country,
        target_country,
        count(distinct primary_group) as num_shared_groups,
        sum(attacks_in_target) as total_spillover_attacks,
        avg(expansion_lag_years) as avg_expansion_lag_years,
        
        -- Spillover score
        count(distinct primary_group) * sum(attacks_in_target) as spillover_intensity_score
        
    from cross_border_pairs
    group by source_country, target_country
)

select * from spillover_intensity
where num_shared_groups >= 2  -- Only meaningful spillovers
order by spillover_intensity_score desc
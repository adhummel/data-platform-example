-- models/intermediate/int_spatial_hotspots.sql
-- Geographic hotspots with intensity scores

{{
  config(
    materialized='table',
    schema='intermediate'
  )
}}

with recent_window as (
    -- Last 3 years
    select *
    from {{ ref('int_gtd_enriched') }}
    where year >= (select max(year) - 2 from {{ ref('int_gtd_enriched') }})
),

country_metrics as (
    select
        country,
        region,
        latitude,
        longitude,
        
        -- Frequency metrics
        count(*) as incidents_recent,
        count(*) / 3.0 as incidents_per_year,
        
        -- Lethality metrics
        sum(total_casualties) as casualties_recent,
        avg(total_casualties) as avg_casualties_per_incident,
        
        -- Attack characteristics
        sum(case when had_suicide then 1 else 0 end) as suicide_attacks,
        sum(case when is_high_impact then 1 else 0 end) as high_impact_attacks,
        count(distinct primary_group) as num_active_groups,
        
        -- Spatial concentration
        count(distinct city) as num_affected_cities,
        stddev(latitude) as lat_spread,
        stddev(longitude) as lon_spread
        
    from recent_window
    where latitude is not null and longitude is not null
    group by country, region, latitude, longitude
),

with_scores as (
    select
        *,
        -- Composite hotspot score (0-100)
        least(100, 
            (incidents_per_year / (select max(incidents_per_year) from country_metrics) * 40) +
            (avg_casualties_per_incident / (select max(avg_casualties_per_incident) from country_metrics) * 30) +
            (high_impact_attacks / nullif(incidents_recent, 0) * 30)
        ) as hotspot_intensity_score,
        
        -- Classification
        case
            when incidents_per_year > 50 and avg_casualties_per_incident > 10 then 'Critical'
            when incidents_per_year > 20 then 'High'
            when incidents_per_year > 5 then 'Moderate'
            else 'Low'
        end as threat_level,
        
        -- Spatial density
        case
            when coalesce(lat_spread, 0) < 1 and coalesce(lon_spread, 0) < 1 
                then 'Concentrated'
            else 'Dispersed'
        end as spatial_pattern
        
    from country_metrics
)

select * from with_scores
order by hotspot_intensity_score desc
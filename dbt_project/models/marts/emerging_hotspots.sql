-- models/marts/mart_emerging_hotspots.sql
-- Answer: "Where are terrorism hotspots emerging?"

{{
  config(
    materialized='table',
    schema='marts'
  )
}}

select
    h.country,
    h.region,
    h.latitude,
    h.longitude,
    h.hotspot_intensity_score,
    h.threat_level,
    
    -- Current metrics
    h.incidents_recent,
    h.casualties_recent,
    h.num_active_groups,
    
    -- Trend from time series
    t.trend_direction,
    t.incidents_yoy_pct_change,
    t.incidents_acceleration,
    
    -- Classification
    case
        when t.trend_direction = 'Accelerating' and h.hotspot_intensity_score > 50
            then 'Emerging Critical Hotspot'
        when t.trend_direction = 'Accelerating'
            then 'Emerging Hotspot'
        when h.threat_level = 'Critical'
            then 'Established Hotspot'
        else 'Stable'
    end as hotspot_status
    
from {{ ref('int_spatial_hotspots') }} h
left join {{ ref('int_region_time_series') }} t
    on h.region = t.region
    and t.year = (select max(year) from {{ ref('int_region_time_series') }})
where h.hotspot_intensity_score > 20  -- Filter noise
order by h.hotspot_intensity_score desc
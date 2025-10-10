-- models/intermediate/int_predictive_features.sql
-- Feature engineering for predictive modeling

{{
  config(
    materialized='table',
    schema='intermediate'
  )
}}

with base_time_series as (
    select
        country,
        region,
        year,
        count(*) as incidents,
        sum(total_casualties) as casualties,
        sum(case when had_suicide then 1 else 0 end) as suicide_attacks,
        count(distinct primary_group) as active_groups
    from {{ ref('int_gtd_enriched') }}
    group by country, region, year
),

with_lags as (
    select
        *,
        
        -- Lagged features (t-1, t-2, t-3)
        lag(incidents, 1) over (partition by country order by year) as incidents_lag1,
        lag(incidents, 2) over (partition by country order by year) as incidents_lag2,
        lag(incidents, 3) over (partition by country order by year) as incidents_lag3,
        
        lag(casualties, 1) over (partition by country order by year) as casualties_lag1,
        lag(casualties, 2) over (partition by country order by year) as casualties_lag2,
        
        -- Moving averages (3-year, 5-year)
        avg(incidents) over (
            partition by country 
            order by year 
            rows between 2 preceding and current row
        ) as incidents_ma3,
        
        avg(incidents) over (
            partition by country 
            order by year 
            rows between 4 preceding and current row
        ) as incidents_ma5,
        
        -- Trend indicators
        (incidents - lag(incidents, 1) over (partition by country order by year)) 
            as incidents_delta,
        
        -- Volatility (rolling standard deviation)
        stddev(incidents) over (
            partition by country 
            order by year 
            rows between 2 preceding and current row
        ) as incidents_volatility,
        
        -- Momentum (rate of change)
        case 
            when lag(incidents, 1) over (partition by country order by year) > 0 
            then (incidents - lag(incidents, 1) over (partition by country order by year)) / 
                 lag(incidents, 1) over (partition by country order by year) 
            else 0 
        end as incidents_momentum,
        
        -- Seasonal indicators (did prior year have spike?)
        case 
            when lag(incidents, 1) over (partition by country order by year) > 
                 avg(incidents) over (partition by country order by year rows between 4 preceding and 2 preceding) * 1.5
            then 1 else 0 
        end as prior_year_spike
        
    from base_time_series
),

with_spatial_features as (
    select
        w.*,
        
        -- Regional context
        avg(w.incidents) over (partition by w.region, w.year) as regional_avg_incidents,
        w.incidents / nullif(avg(w.incidents) over (partition by w.region, w.year), 0) 
            as country_to_region_ratio,
        
        -- Neighbor effects (proxy: region spillover)
        sum(w.incidents) over (partition by w.region, w.year) - w.incidents 
            as neighbor_incidents
        
    from with_lags w
)

select * from with_spatial_features
where year >= 1975  -- Ensure we have lag features
order by country, year
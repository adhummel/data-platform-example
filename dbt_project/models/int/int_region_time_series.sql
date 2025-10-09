{{
  config(
    materialized='table',
    schema='intermediate'
  )
}}

with base as (
    select
        region,
        year,
        count(*) as incidents,
        sum(num_killed) as casualties_killed,
        sum(num_wounded) as casualties_wounded,
        sum(total_casualties) as casualties_total,
        avg(total_casualties) as avg_casualties_per_incident
    from {{ ref('int_gtd_enriched') }}
    group by region, year
),

with_lags as (
    select
        *,
        -- Prior period values for comparison
        lag(incidents, 1) over (partition by region order by year) as incidents_prev_year,
        lag(casualties_total, 1) over (partition by region order by year) as casualties_prev_year,
        
        -- 3-year moving averages
        avg(incidents) over (
            partition by region 
            order by year 
            rows between 2 preceding and current row
        ) as incidents_3yr_avg,
        
        avg(casualties_total) over (
            partition by region 
            order by year 
            rows between 2 preceding and current row
        ) as casualties_3yr_avg
    from base
),

with_acceleration as (
    select
        *,
        -- Year-over-year change
        incidents - coalesce(incidents_prev_year, incidents) as incidents_yoy_change,
        round(100.0 * (incidents - coalesce(incidents_prev_year, incidents)) / 
              nullif(incidents_prev_year, 0), 2) as incidents_yoy_pct_change,
        
        casualties_total - coalesce(casualties_prev_year, casualties_total) as casualties_yoy_change,
        
        -- Acceleration (change in rate of change)
        incidents - incidents_3yr_avg as incidents_acceleration,
        
        -- Volatility (standard deviation over 3 years)
        stddev(incidents) over (
            partition by region 
            order by year 
            rows between 2 preceding and current row
        ) as incidents_volatility,
        
        -- Trend direction
        case
            when incidents > incidents_3yr_avg * 1.2 then 'Accelerating'
            when incidents < incidents_3yr_avg * 0.8 then 'Declining'
            else 'Stable'
        end as trend_direction
        
    from with_lags
)

select * from with_acceleration
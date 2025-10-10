-- models/marts/mart_forecasting_dataset.sql
-- Answer: "Can we predict next attacks?" (Training data)

select
    country,
    region,
    year,
    
    -- Target variable (what we want to predict)
    incidents as target_incidents_next_year,
    
    -- Features
    incidents_lag1,
    incidents_lag2,
    incidents_lag3,
    incidents_ma3,
    incidents_ma5,
    incidents_delta,
    incidents_momentum,
    incidents_volatility,
    casualties_lag1,
    suicide_attacks,
    active_groups,
    regional_avg_incidents,
    country_to_region_ratio,
    neighbor_incidents,
    prior_year_spike
    
from {{ ref('int_predictive_features') }}
where incidents_lag1 is not null  -- Only rows with full feature set
order by country, year
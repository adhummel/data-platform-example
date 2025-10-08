# Data Dictionary

## Source Data: Global Terrorism Database

### Key Fields from GTD

| Field | Type | Description |
|-------|------|-------------|
| eventid | TEXT | Unique incident identifier |
| iyear | INTEGER | Year of incident |
| imonth | INTEGER | Month of incident (1-12) |
| iday | INTEGER | Day of incident (1-31) |
| country_txt | TEXT | Country name |
| region_txt | TEXT | Geographic region |
| city | TEXT | City name |
| latitude | NUMERIC | Latitude coordinate |
| longitude | NUMERIC | Longitude coordinate |
| attacktype1_txt | TEXT | Primary attack type |
| targtype1_txt | TEXT | Primary target type |
| weaptype1_txt | TEXT | Primary weapon type |
| nkill | INTEGER | Number killed |
| nwound | INTEGER | Number wounded |
| gname | TEXT | Perpetrator group name |
| summary | TEXT | Incident description |

## Marts Layer

### fct_incidents
Fact table containing all terrorism incidents.

| Column | Type | Description |
|--------|------|-------------|
| incident_id | TEXT | Unique incident identifier |
| incident_date | DATE | Date of incident |
| location_key | TEXT | FK to dim_locations |
| group_key | TEXT | FK to dim_groups |
| attack_type_key | TEXT | FK to dim_attack_types |
| target_type | TEXT | Primary target category |
| weapon_type | TEXT | Primary weapon used |
| casualties_killed | INTEGER | Number of fatalities |
| casualties_wounded | INTEGER | Number of injuries |
| total_casualties | INTEGER | Total killed + wounded |
| is_suicide | BOOLEAN | Suicide attack indicator |
| is_success | BOOLEAN | Attack success indicator |

### dim_locations
Dimension table for geographic locations.

| Column | Type | Description |
|--------|------|-------------|
| location_key | TEXT | Surrogate key |
| country | TEXT | Country name |
| region | TEXT | Geographic region |
| city | TEXT | City name |
| latitude | NUMERIC | Latitude |
| longitude | NUMERIC | Longitude |

### dim_groups
Dimension table for perpetrator groups.

| Column | Type | Description |
|--------|------|-------------|
| group_key | TEXT | Surrogate key |
| group_name | TEXT | Organization name |
| first_attack_date | DATE | First recorded attack |
| last_attack_date | DATE | Most recent attack |
| total_attacks | INTEGER | Number of attacks |
| total_casualties | INTEGER | Total casualties caused |

### metrics_regional
Regional aggregated metrics.

| Column | Type | Description |
|--------|------|-------------|
| region | TEXT | Geographic region |
| year | INTEGER | Year |
| incident_count | INTEGER | Number of incidents |
| total_killed | INTEGER | Total fatalities |
| total_wounded | INTEGER | Total injuries |
| avg_casualties_per_incident | NUMERIC | Average casualties |

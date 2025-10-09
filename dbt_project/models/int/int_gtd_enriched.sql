{{
  config(
    materialized='table',
    schema='intermediate'
  )
}}

/*
  Enriched GTD dataset combining all staging models.
  This intermediate model serves as the foundation for all downstream analysis.

  Joins:
  - stg_attack_results (base): casualty data, success flags, dates
  - stg_attack_location: geographic information
  - stg_attack_actors: perpetrator group information
  - stg_attack_targets: target information
  - stg_attack_weapons: weapon details
*/

with results as (
    select * from {{ ref('stg_attack_results') }}
),

location as (
    select * from {{ ref('stg_attack_location') }}
),

actors as (
    select * from {{ ref('stg_attack_actors') }}
),

targets as (
    select * from {{ ref('stg_attack_targets') }}
),

weapons as (
    select * from {{ ref('stg_attack_weapons') }}
),

enriched as (
    select
        -- Primary key
        results.event_id,

        -- Time dimension (from results)
        results.year,
        results.approx_date,

        -- Location dimensions (from location)
        location.country_id,
        location.country,
        location.region_id,
        location.region,
        location.province_state,
        location.city,
        location.latitude,
        location.longitude,
        location.specificity,
        location.vicinity,
        location.location,

        -- Actor dimensions (from actors)
        actors.primary_group,
        actors.subgroup,
        actors.secondary_group,
        actors.tertiary_group,

        -- Target dimensions (from targets)
        targets.target_category,
        targets.target_subcategory,
        targets.target_corporation,
        targets.target_name,
        targets.target_nationality,

        -- Weapon dimensions (from weapons)
        weapons.weapon_type_id,
        weapons.weapon_type,
        weapons.weapon_description,

        -- Results & casualties (from results)
        results.num_killed,
        results.num_wounded,
        results.num_perpetrators,
        results.num_properties_damaged,
        results.was_successful,
        results.had_suicide,
        results.motive,
        results.summary,

        -- Calculated fields
        coalesce(results.num_killed, 0) + coalesce(results.num_wounded, 0) as total_casualties,

        -- Severity flags
        case
            when coalesce(results.num_killed, 0) + coalesce(results.num_wounded, 0) = 0 then 'No Casualties'
            when coalesce(results.num_killed, 0) + coalesce(results.num_wounded, 0) <= 5 then 'Low'
            when coalesce(results.num_killed, 0) + coalesce(results.num_wounded, 0) <= 25 then 'Medium'
            when coalesce(results.num_killed, 0) + coalesce(results.num_wounded, 0) <= 100 then 'High'
            else 'Extreme'
        end as severity_category,

        -- Attack characteristics
        case
            when results.had_suicide then 'Suicide Attack'
            when targets.target_category in ('Government (General)', 'Military') then 'Government/Military Target'
            when targets.target_category in ('Private Citizens & Property', 'Business') then 'Civilian Target'
            else 'Other'
        end as attack_type_category

    from results
    left join location on results.event_id = location.event_id
    left join actors on results.event_id = actors.event_id
    left join targets on results.event_id = targets.event_id
    left join weapons on results.event_id = weapons.event_id
)

select * from enriched

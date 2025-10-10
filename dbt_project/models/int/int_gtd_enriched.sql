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

        -- Simplified target type
        case
            when targets.target_category ilike '%government%' or targets.target_category ilike '%police%' or targets.target_category ilike '%law enforcement%' then 'Government/Law Enforcement'
            when targets.target_category ilike '%military%' or targets.target_category ilike '%armed%' then 'Military/Armed Groups'
            when targets.target_category ilike '%citizen%' or targets.target_category ilike '%civilian%' then 'Civilians'
            when targets.target_category ilike '%business%' or targets.target_category ilike '%infrastructure%' or targets.target_category ilike '%utilities%' then 'Infrastructure/Business'
            else 'Other'
        end as target_type_simplified,

        -- Weapon dimensions (from weapons)
        weapons.weapon_type_id,
        weapons.weapon_type,
        weapons.weapon_description,

        -- Simplified weapon category
        case
            when weapons.weapon_type ilike '%explosive%' or weapons.weapon_type ilike '%bomb%' then 'Explosives'
            when weapons.weapon_type ilike '%firearm%' or weapons.weapon_type ilike '%gun%' or weapons.weapon_type ilike '%rifle%' then 'Firearms'
            when weapons.weapon_type ilike '%incendiary%' or weapons.weapon_type ilike '%fire%' then 'Fire/Incendiary'
            when weapons.weapon_type ilike '%melee%' or weapons.weapon_type ilike '%knife%' then 'Melee'
            when weapons.weapon_type ilike '%vehicle%' then 'Vehicle'
            else 'Other'
        end as weapon_category,

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
        end as attack_type_category,

        -- High impact flag (high or extreme severity)
        case
            when coalesce(results.num_killed, 0) + coalesce(results.num_wounded, 0) > 25 then true
            else false
        end as is_high_impact

    from results
    left join location on results.event_id = location.event_id
    left join actors on results.event_id = actors.event_id
    left join targets on results.event_id = targets.event_id
    left join weapons on results.event_id = weapons.event_id
)

select * from enriched

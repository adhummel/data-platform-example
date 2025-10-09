select *
from {{ source('raw', 'gtd_incidents')}}
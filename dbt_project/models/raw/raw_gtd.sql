select *
from {{ source('data_raw', 'gtd_incidents')}}
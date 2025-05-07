
  create or replace   view f1_db.raw.my_second_dbt_model
  
   as (
    -- Use the `ref` function to select from other models

select *
from f1_db.raw.my_first_dbt_model
where id = 1
  );


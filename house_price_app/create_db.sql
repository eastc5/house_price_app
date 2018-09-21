CREATE DATABASE land_registry_uk;
begin;
create table land_registry_price_paid_uk(
  transaction uuid,
  price numeric,
  transfer_date date,
  postcode text,
  property_type char(1),
  newly_built boolean,
  duration char(1),
  paon text,
  saon text,
  street text,
  locality text,
  city text,
  district text,
  county text,
  ppd_category_type char(1));

copy land_registry_price_paid_uk FROM '/home/pg/Downloads/pp-complete.csv' with (format csv, freeze true, encoding 'win1252', header false, null '', quote '"', force_null (postcode, saon, paon, street, locality, city, district));
commit;

CREATE INDEX land_registry_price_paid_uk_postcode_idx ON land_registry_price_paid_uk (postcode);

CREATE USER your_readonly_user  WITH ENCRYPTED PASSWORD 'your_readonly_password';
GRANT USAGE ON SCHEMA public to your_readonly_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO your_readonly_user;

GRANT CONNECT ON DATABASE land_registry_uk to your_readonly_user;
\c land_registry_uk
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO your_readonly_user; --- this grants privileges on new tables generated in new database "land_registry_uk"
GRANT USAGE ON SCHEMA public to your_readonly_user; 
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO your_readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO your_readonly_user;

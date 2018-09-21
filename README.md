# House Price App

Playing around with flask and postgres

The files here create a very simple app which allows
you to enter a UK postcode and get back all the
transactions for all houses in that post code dating back to 
1995-ish

The data for this came from here: http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv

Its is a big file 3.5 GB. Learn everything you need to about it from here https://www.gov.uk/guidance/about-the-price-paid-data

create_db.sql creates a local postgres db. You will have to install postgres yourself
(i used version 9.5.14 ) first. Run the script with root credentials and it will set up the database (importing from the csv of the data) and set up the read only user. You will then need to populate a .config.yaml file with the credentials you set in the postgres.sql script so the db connection string is correct.

then run 
```
export FLASK_APP=house_price_app
flask run
```

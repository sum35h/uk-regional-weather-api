# uk-regional-weather-api

## Description
This project is a DRF application to serve time-series of monthly, seasonal and annual values from https://www.metoffice.gov.uk/research/climate/maps-and-data/uk-and-regional-series#yearOrdered


## PIP dependencies
```
pip install -r requirements.txt

```
## Database setup
Create a .env file in the climate_science directory containing all the macros if needed

## Database setup
Configure Postgres db in the settings.py
```
python manage.py migrate
python manage.py makemigrations
python manage.py migrate 
```

## ETL Command
ETL script to ingest the data asynchronously
```
python manage.py etl_data
```

### URL endpoints

#### GET /api/data/\<string:parameter\>/monthly/\<string:region\>
Fetch the monthly time-series json of a region 
```
Ex:
/api/data/Tmean/monthly/UK
```
#### GET /api/data/\<string:parameter\>/seasonal/\<string:region\> 
Fetch the seasonal time-series json of a region 
```
Ex:
/api/data/Tmean/seasonal/UK
```
#### GET /api/data/\<string:parameter\>/monthly/\<string:region\>
Fetch the annual time-series json of a region 
```
Ex:
/api/data/Tmean/annual/UK
```

#### GET /api/data/\<string:parameter\>/monthly/\<string:region\>?year_range=1999,2012 
Filter the monthly time-series json of a region by year
```
Ex:
/api/data/Tmean/annual/UK?year_range=1999,2012
```

## Django Server
```
python manage.py runserver
```

## Testing
```
python manage.py test
```



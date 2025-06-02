# Data preparation service

This services is mainly meant for development, during which the base/historical data might still evolve. After launch for production, the service can be used in exceptional circumstances (i.e., app has been down for some reason) to populate database.

## Data directory

Holds `.csv` and `.xslx` files for bulk loading to database tables.

## Scripts directory

Holds the scripts for fetching data from external sources and for populating the database.

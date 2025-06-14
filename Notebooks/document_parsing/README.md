# Document parsing and loading

## Dependecies

In `Eprice/Notebooks/` run `uv sync` -- this installs everything you need (and then some...). Activate the env before running any scripts, or select the appropriate kernel if you use the notebooks.

The project database needs to be up and running before trying to populate it. So, you need to either run compose up like you'd do to access the app, or spin up the db alone with `docker compose up -d database`.

## Contents

Here are the most basic tools to parse the project source code and documentation, save them in text format, and clean and prepare for embedding and insertion to database. There are various scripts and some notebooks for offline population of the db.

The embedding models are open source, so you don't need any api keys. The database container has to be running in order to load the data. If you want to update the data, use the `document_loading.ipynb` notebook or `parse_project.sh` -- both achieve the same result. See comments and commented-out code blocks for advice -- or better yet, as Paavo...


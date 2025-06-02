# Document parsing and loading

Here are the most basic tools to parse the project source code and documentation, save them in text format, and clean and prepare for embedding and insertion to database. There are various scripts and some notebooks for offline population of the db.

The embedding models are open source, so you don't need any api keys. The database container has to be running in order to load the data. If you want to update the data, first truncate the old tables -- or, you can also remove `Eprice/App/pgdata` folder, and then re-populate the database (truncation is easier).

To remove the old datum:

```bash
docker exec -it postgresql_database psql  # go inside the container
```

inside the container:

```postgres
\dt -- check the relevant tables
TRUNCATE TABLE <table_name>;
TRUNCATE TABLE <table_name> CASCADE; -- need to cascade for langchain_pg_collection/-embedding
```

After removing the old data, use the `document_loading.ipynb` notebook. See comments and commented-out code blocks for advice -- or better yet, as Paavo...

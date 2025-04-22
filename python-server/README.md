## Python FastAPI server template for Eprice app

You need to define `.env` -file for production. The defaults should work for development purposes. See config folder.

* requirements.txt has all the requirements -- if you add more, upodate the requirements.

* this is meant to be launched by docker compose from parent folder.

### Dockerized

The server is meant to be run  from docker container, and it is using dockerized Postgres database by default. It is also possible to develop it without docker by setting up an independent Postgres database, by running the postgres container, or by ignoring the database for unrelated dev. You can also define you own SQLite database locally form the python-server -- just change how the repositories make the connection.

* .dockerignore has the basics, but if you use some other .venv naming convention, add them. The container uses pip and requirements to install dependencies -- so using managers like uv/pip/poetry might produce files/folders you must exclude from docker (it copies all contents not excluded in the container).

* .gitignore, same things. No venv's or lock files.

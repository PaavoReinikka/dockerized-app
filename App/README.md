# Eprice App

The Eprice App is a containerized application that allows users to view the market price of electricity in Finland, both current and historical. The app is built with a modern tech stack, including a Svelte frontend, a FastAPI backend, a PostgreSQL database, and various tools for testing and data management.

## Features

- **Electricity Price Viewer**: View current and historical electricity prices in Finland.
- **Svelte Frontend**: A modern, responsive UI built with Svelte and Vite.
- **FastAPI Backend**: A Python-based backend for handling API requests and business logic.
- **PostgreSQL Database**: A robust database for storing electricity price data.
- **Flyway Migrations**: Manage database schema changes with ease.
- **Testing**: End-to-end tests with Playwright and backend API tests with Pytest.
- **User chat**: A chat-based interface to help with the functionalities of the app.
- **Data Loading**: Load and update electricity price data into the database using scripts in a dedicated container.

---

## Project Structure
.

 ├── README.md # Root README file

 ├── compose.yaml # Docker Compose configuration 
 
 ├── user-chat/ # Chat engine service 
 
 ├── client/ # Svelte frontend service
 
 ├── data-preparation/ # Scripts and data for populating the database
 
 ├── database-migrations/ # Flyway migration scripts 
 
 ├── e2e-tests/ # Playwright end-to-end tests
 
 ├── python-server/ # FastAPI backend service
 
 └── project.env # Environment variables for the project


---

## Getting Started

### Prerequisites

- **Docker** and **Docker Compose**: Install Docker Desktop or Docker CLI.
- **Deno**: Required for local development of the frontend (see `client/README.md`), and package management.

Any libraries needed in the containers are installed automatically using requirements or other configuration files. `uv` is preferable package manager also inside containers, but pip is used as fallback in some cases.

### Database Persistence

To ensure your PostgreSQL database data is persisted locally (so it is not lost when containers are stopped or removed), you need to create a directory for the database files and set the correct permissions:

```bash
mkdir -p ./pgdata
chmod 700 ./pgdata
sudo chown -R 999:999 ./pgdata
```

- `mkdir -p ./pgdata` creates the directory if it doesn't exist.
- `chmod 700 ./pgdata` sets secure permissions (Postgres default).
- `sudo chown -R 999:999 ./pgdata` sets ownership to the default Postgres user inside the container (UID 999).

**Alternatively**, if you do not want to populate the database yourself you can unpack the tar file and use that as your pgdata -- the archive includes everything the developer chat needs, but it is the frozen state of the project at 2025-6-7.

```bash
tar xzvf pgdata.tar.gz
```

Just ensure your Compose file mounts ./pgdata:/var/lib/postgresql/data -- you also need to set the permissions like it is explained above. Similarly, if you update the database yourself and want to take a snapshot, run:

```bash
tar czvf pgdata.tar.gz pgdata
```

**Note:**  
If you change to a custom Postgres image or user, check the UID/GID with:

```bash
docker run --rm <root/image:version> id postgres
```
(here we have root=reinikp2 and image=pgvector-database, and version=v1)

and adjust the `chown` command accordingly.

### Running the App

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd Eprice
    ```

2. Build and start the containers:
    ```bash
    docker compose up --build
    ```

3. Access the services:

* Frontend: http://localhost:5173
* Backend: http://localhost:8000

4. To stop the containers:
    ```bash
    docker compose down
    ```

### Testing


1. Run Playwright tests:
    ```bash
    docker compose run --rm --entrypoint=npx e2e-tests playwright test
    ```

2. Run Pytest for backend API (using uv inside the container):
    ```bash
    docker compose run backend-tests [uv run pytest]
    ```

### Environment Variables

* Use `.env.local` for local development (gitignored)

* Use `project.env` for containerrized development

* To inspect environment variables inside a container:
    ```bash
    docker exec -it <container_name> bash
    printenv
    ```

### Services overview

1. Frontend (Client)
Built with Svelte and Vite.
Located in the client/ directory.
See client/README.md for more details.

2. Backend (Python Server)
Built with FastAPI.
Located in the python-server/ directory.
See python-server/README.md for more details.

3. Database
PostgreSQL database for storing electricity price data.
Flyway is used for managing schema migrations (database-migrations/).

4. User Chat
A chat-based interface for interacting with the app.
Located in the user-chat/ directory.

5. Data Preparation
Scripts for loading and updating electricity price data.
Located in the data-preparation/ directory.

### Contributing

1. Fork the repository.

2. Create a feature branch:

    ```bash
    git checkout -b feature-name
    ```

3. Commit your changes:

    ```
    git commit -m "Add feature-name"
    ```

4. Push to your branch:

    ```bash
    git push origin feature-name
    ```

5. Open pull request.


## License

This project us under MIT license: https://mit-license.org/

## Acknowledgments

Electricity price data is sourced from Pörssisähkö API.

## Additional notes

**Install docker and docker compose**. Maybe easiest to just install docker desktop, especially on windows.

**Postgres is not needed on local machine** (unless you want to run outside containers).

The compose.yaml and the individual Dockerfiles are sufficient to run the App. Docker does the installing for the containers. But you can still run `deno install --allow-scripts`, if you want to run on local host. On windows, after running deno install, `node_modules/` that are loaded into client should not be copied into the container -- the container is using arch-linux as base image. You can either remove those, or add your own `.dockerignore` file.

Run using docker compose:

`docker compose up --build` (no need to build everytime)

You can also simply `ctrl+C` to shut down the containers, or

`docker compose down` to tear down.


### **About environment variables**

Keep private information private, preferably :-). You can use `.env.local` convention, and keep them gitignored. For public api keys, while developing, we can all get our own api keys.

**If you are unsure what environment variables are loaded on your container launch -- either by docker from project.env, or by services using other tools, like dotenv -- you can always go inside the container to check:**

```
docker compose up -d <service_name> # launch the container

docker exec -it <container_name> bash # go into cmdline inside

(container): printenv # or echo etc.
```

**For developing client:** There is a sort of a bug in the denolands alpine image, which prevents us from installing with optional flags -- in our case `deno install --allow-scripts`. This means that the node modules need to be copied from local. This is not an issue if you are using linux (or wsl2 on Windows). Later, there might be a change in the client's base image later on to fix this issue.

And note that the container names are not necessarily same as the service name (they are derived from it though); you can check running cont's with `docker <container> ps`.

### Running without Docker

Can be done, but needlessly cumbersome. Ask Paavo for the how.


### Starting a new client build from scratch

If you want to start the client build from scratch, for example with typescript checking enabled, run:

```bash
deno run -A npm:sv@latest create client
```

from the root directory, and choose from the given options. For this project, we have used the most minimal build setup (SveleteKit minimal, no TS typechecking, nothing added, with deno itself for dependency management).

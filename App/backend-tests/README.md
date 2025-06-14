# Endpoint tests

Tests for the phase of development when the frontend is incomplete. Helps in picking up on errors, exceptions and warnings. Relies on Pydantic and proper exception ahndling in the backend to be fully informative. Becomes somewhat obsolete after e2e-tests have been written.

You need to have the Eprice -app running if you want to run the tests. So call `docker compose up` to run the server (or with `-d server` flag, since front is not needed for these tests). If you run `docker compose up --build`, the backend tests **will not be started** as they are defined as a "profile" in compose file.

To run the tests, first build the container with `docker compose build` inside the backend-tests, or just by adding the `--build` and `-d` flags:

```
docker compose up --build -d backend-tests
```

You can also run them in various other ways, e.g., jointly with every other container:

```
docker compose up --profile backend-tests
```

If you do it this way, and we add tests that depend on the loaded data in the database, this can cause issues -- we need to specify in the compose file that the backend-tests depends on `database: service_healthy`.

You can also run the tests with

```
docker compose run backend-tests
```

but these will leave a "orphan" containers behind -- these can be removed with `--remove-orphans` flag. Docker will warn you is this is happening, and in any case it is good practice to keep an eye on dockers resource usage and dangling containers:

```
docker ps # running containers
docker ps -a # all containers
docker inspect <container_name_or_id>
docker stats # resource usage
docker container prune # remove stopped containers (it prompts you)
docker system prune # remove unused images, networks (and volumes)
```

## Tested Endpoints and Features

| Endpoint                 | HTTP | Description                                 |
|--------------------------|------|---------------------------------------------|
| /api/auth/register       | POST | User registration                           |
| /api/auth/login          | POST | Login                                      |
| /api/auth/logout         | GET  | Logout                                     |
| /api/public/data         | GET  | Public price data                           |
| /api/data/today          | GET  | Today's price data                          |
| /api/price/range         | POST | Price data for a time range                 |
| /api/price/hourlyavg     | POST | Hourly average prices for a time range      |
| /api/price/weekdayavg    | POST | Weekday average prices for a time range     |
| /api/windpower           | GET  | Wind power production data                  |
| /api/windpower/range     | POST | Wind power production data for a time range |
| /api/consumption         | GET  | Electricity consumption data                |
| /api/consumption/range   | POST | Electricity consumption data for a time range|
| /api/production          | GET  | Total electricity production data           |
| /api/production/range    | POST | Total electricity production data for a time range|


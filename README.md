### Containerized Eprice app template

**Install docker and docker compose**. Maybe easiest to just install docker desktop, especially on windows.

**Postgres is not needed on local machine** (unless you want to run outside containers).

**Install Deno** (see client folder).

The compose.yaml and the individual Dockerfiles are sufficient to run the App. Docker does the installing for the containers. But you can still run `deno install --allow-scripts`, if you want to run on local host. On windows, after running deno install, `node_modules/` that are loaded into client should not be copied into the container -- the container is using arch-linux as base image. You can either remove those, or add your own `.dockerignore` file.

Run using docker compose:

`docker compose up --build` (no need to build everytime)

You can also simply `ctrl+C` to shut down the containers, or

`docker compose down` to tear down.

#### Chat-engine

Chat-engine is still just a minimal skeleton using `gradio` dashboard and an iframe. When I find the time, I'll start adding a bit more to it. It is using ollama, and you need to create a folder `chat-engine/.ollama` which will be mounted by compose. **You do not need ollama on the host.**

By default, compose will not spin the chat-engine up, that has to be done by choosing a profile:

`docker compose --profile chat-engine up`.

It has to load the `llama3.2` model (although you can use the model you like), so it takes some time the first time around. File `chat-engine/run.sh` does the model pull, and you may end up having to tweak it yourself.

#### Chat-engine without docker

Install ollama (https://ollama.com/) and check that it's serving, e.g., by running `curl localhost:11434`. Then pull a model, e.g., `ollama pull llama3.2:latest`. Then, either using pip (see dependencies in pyproject.toml), or *preferably* 😊 use uv (https://docs.astral.sh/uv/getting-started/installation/) and run `uv sync` in chat-engine folder.

And run the engine with

`uv run gradio_dashboard.py` or `python gradio_dashboard.py`.

It serves on `port=7860`.

### Python-server without docker

If you want to run the server without docker, make a virtualenv, install dependencies with `pip install -r requirements`, or use some other tool. Later on, I'll update the project to use uv, since it's just way faster.

With dependecies installed, and (potentially) venv active, run something like:

`uvicorn main:app --host localhost --port 8000 --reload`

(the `--reload` ensures that whenever you update the code, the effect is reflected on the server).


#### Run the Playwright e2e tests; just a skeleton -- add more as you go.

When the containers are up and running, in another terminal run:

`docker compose run --rm --entrypoint=npx e2e-tests playwright test`

Perhaps eventually modify the compose.yaml so that the tests are automatically run when the app is launched.

#### Running client without Docker

Basic `deno run dev --host` is sufficient for the client. 

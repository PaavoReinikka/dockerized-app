## Chat engine for Eprice app

This folder has the dockerfile for ollama llm engine, and a minimal gradio dashboard implementation. In order to run the engine, docker needs to load the *llama3.2* model first. It will be downloaded into `chat-engine/.ollama/` folder, which you need to create. However, do not include it in git. 

The chat-engine uses uv as the default package manager, and it's included in the container also. The dependencies are in `pyproject.toml`, and if you prefer pip, you can always you that. However, remember to include you local virtualenvironment into .gitignore and .dockerignore.

**This container is not run by default when you run the project using docker-compose**. To include the chat-engine, you need use a specific profile:

```
docker compose --profile chat-engine up
```

You should have `chat-engine/.env.development` with `OPENAI_API_KEY` defined -- it does not need to be a valid api key, any styring will do. This is due to llm client/interface compatibility (and only for now). Eventually, we will collect all env files into a single project env (at compose level).

The bash script `run.sh` is likely going to change before long, but for now it's used to manage the Ollama server inside the container. You can connect directly into the container with `docker exec -it chat-engine bash` or something of that nature.

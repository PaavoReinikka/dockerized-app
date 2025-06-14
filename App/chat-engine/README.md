# Eprice Chat Engine

This folder contains the **chat engine** for the Eprice app. The chat engine provides a knowledge base chat interface for the Eprice project, allowing users to interact with project documents, retrieve files, and generate PlantUML diagrams via a conversational interface.

## Features

- **Conversational AI**: Uses OpenAI's GPT models (via LangChain) for chat and document reranking.
- **Document Search & Reranking**: Retrieves relevant project documents using a HuggingFace embedding model (`BAAI/bge-small-en`) and reranks them with an LLM.
- **File Retrieval**: Allows users to fetch project files by name.
- **PlantUML Diagram Generation**: Generates and displays UML diagrams from code or files.
- **Streaming Responses**: Supports streaming chat responses for a responsive UI.
- **Gradio UI**: Provides a web-based chat and file browser interface using Gradio.

## Architecture

- **Embedding Model**: Uses HuggingFace's `BAAI/bge-small-en` for vector search.
- **LLM**: Uses OpenAI's GPT models (e.g., `gpt-4o-mini`) via LangChain's `ChatOpenAI`.
- **Vector Store**: Uses the project's PostgreSQL database (via `langchain_postgres.PGVector`) for storing and searching document embeddings.
- **Reranking**: LLM-based reranking of search results for improved relevance.
- **Tools**: Exposes tools for document search, file retrieval, and diagram generation to the agent.

## Components

- `app.py` : Entrypoint for chat, agent and file apps.
- `chat_app.py`: Gradio chat interface for the knowledge base.
- `agent_app.py`: Gradio app with agent-based chat and UML diagram viewer.
- `file_app.py`: Gradio app for browsing and viewing project files.
- `chat_manager_with_tools.py` / `agent_manager.py`: Core logic for chat, retrieval, reranking, and tool integration.
- `autoloading_uml.py`: Gradio component for live UML diagram rendering.
- `utils/`: Helper functions and tool definitions.

## Setup

By default, compose does everything. If you read the `Eprice/App/README.md` and followed the instructions to extract the archived `pgdata` directory, you should be all set. Otherwise you need to populate chat data yourself -- this needs to be done offline (may change in the future). You can also run the chat locally (see instructions below). The instructions to populate the database are in `Eprice/Notebooks/document_loading`. **If you want to develope the chat, you need to go read `Eprice/Notebooks/document_loading/README.md`**. The notebooks and scripts (which ever you use) will download the required HF model to your local machine, and that will be mounted to the chat container -- this is not strictly necessary, but downloading the model repeatedly during the container on build tends to bump into HF rate limits (nasty traces to debug).

### Prerequisites

- see `pyproject.toml` for dependencies
- `BAAI/bge-small-en` model locally in `~/.cache/hugginface/`
- PostgreSQL database with project documents loaded
- OpenAI API key (for LLM access)
- (Optional) PlantUML JAR for diagram generation

### Installation

1. **Clone the repository** and navigate to `App/chat-engine/`.

2. **Install dependencies** using [uv](https://github.com/astral-sh/uv) (Optional, only for local usage):

   ```bash
   uv sync
   ```

3. **Set up environment variables**:

   Create a `.env.private` file with at least:

   ```
   OPENAI_API_KEY=your-openai-key
   ```

   The database connection is using `Eprice/App/project.env`. For local use/dev you can include everything in your `.env.private`:

   ```
   OPENAI_API_KEY=your-openai-key
   PGHOST=localhost
   PGPORT=5432
   PGUSER=your_pg_user
   PGPASSWORD=your_pg_password
   PGDATABASE=your_pg_db
   ```

4. **(Optional) PlantUML**:  
   For local UML diagram generation, download `plantuml.jar` and place it in your home directory or adjust the path in `autoloading_uml.py`. You may also need to install Graphviz (`sudo apt install graphviz` or similar).

5. **Prepare the database**:  
   Ensure your PostgreSQL database is running and contains the project documents.

## Running the Chat Engine

All commands assume you have an appropriate venv active, or you can replace `python` call with `uv run`. You can launch all apps at once:

```bash
python app.py
```

Or run individual apps:

```bash
python chat_app.py      # Main chat interface
python agent_app.py     # Agent chat + UML viewer
python file_app.py      # File browser
```

## Usage

- Access the Gradio web UI at the address printed in the terminal (http://localhost:7860-63).
- Chat with the agent to ask questions about the project, retrieve files, or request UML diagrams.
- Use the file browser to view project files directly.

## Notes

- The chat engine does **not** require Ollama or any local LLMs. All LLM calls are made via OpenAI's API.
- Embeddings are generated using HuggingFace models locally.
- The chat engine is started by default in Docker Compose. To exclude it, edit the compose file and uncomment the lines in chat-engine service that define it as a profile.
- For development, you may need to adjust paths or environment variables to match your setup.

## Development

- Dependencies are managed via `pyproject.toml` and can be installed with `uv`.
- The code is modular and can be extended with new tools or retrieval strategies.
- See the source files for more details on extending or customizing the chat engine.

---

**For any issues or questions, please contact the Eprice project maintainers.**
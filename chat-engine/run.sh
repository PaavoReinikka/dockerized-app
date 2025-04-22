#!/bin/bash

# you might want to tweak these
export OLLAMA_API_KEY="any_good_old_string_is_ok"

echo "🔴 Starting Ollama..."
ollama serve &
echo "🟢 Ollama started!"

# Wait for Ollama to be ready
echo "🔴 Waiting for Ollama to be ready..."
sleep 5
echo "🟢 Ollama is ready!"

echo "🔴 Retrieving model..."
ollama pull llama3.2
echo "🟢 Done!"


# Start the Gradio app and log output
echo "🔴 Starting Gradio app..."
uv run gradio_dashboard.py


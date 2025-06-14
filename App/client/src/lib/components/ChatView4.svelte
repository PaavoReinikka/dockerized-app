
<div class="container mx-auto p-4">
  <h1 class="text-3xl font-bold mb-4">Developer Chat</h1>
  <p class="mb-4">
    The Developer Chat is based on retrieval augmented generation (RAG) and uses
    the project documentation and code as a knowledge base. It is designed to assist both developers
    and those evaluating the project in understanding the codebase, answering questions, and providing insights.
    There are two chat views available, both based on the same model (OpenAI's gpt-4o-mini).
    Both models keep conversation history, so you can always ask follow-up questions to get more detailed answers.
  </p>
  <p class="mb-4">
    In addition to LLM's, you can also access the code base and documentation yourself.
  </p>
  <h2 class="text-2xl font-bold mb-2">Files</h2>
  <p class="mb-4">
    A view that allows you to scroll through the files in the codebase and documentation.
    You can click on the files to view their contents. Both chat views have access to the same files,
    and understand the directory structure of the codebase.
  </p>
  <h2 class="text-2xl font-bold mb-2">Streaming</h2>
  <p class="mb-4">
    A sreaming chat with access to the documents and the codebase (traditional chat view).
    Based on a user query, the model retrieves relevant code snippets and
    other documentatation related to the query. The retrieved content is then ranked and
    only the most relevant texts are passed to the model as context information.
    The model then generates a response based on the provided context. 
  </p>
    <h2 class="text-2xl font-bold mb-2">Agent</h2>
    <p class="mb-4">
    An agent-based chat that uses the same model as the streaming chat, but with a different approach.
    The agent can access the codebase and documentation using tool-calls, allowing it to retrieve relevant information dynamically.
    This allows for more flexible and dynamic interactions, as the agent can provide insights and answers without being limited to
    pre-defined context. The agent can also perform other actions for the user, such as searching the codebase or documentation,
    and even generate UML diagrams based on the code structure.
  </p>
</div>

# Chroma Vector Store


The Chroma Vector Store node allows you to store and query vectorized documents in a ChromaDB server. It connects to your specified host and port, using a defined collection name to organize indexed data.


### Inputs


- Documents - Accepts vectorized document chunks for storage. These typically come from embedding nodes.
- Questions - Accepts queries (e.g., user prompts or questions) to search the vector database for relevant context.


This guide walks you through configuring Ngrok on your local machine


### Outputs


- Answers - Returns context-relevant document results retrieved from the vector store in response to input questions.
- Documents - Emits the full document metadata or ID associated with retrieved vector matches.
- Questions (output) - Returns the question passed through after retrieval, useful for chaining with LLM nodes.


### Configuration Steps


- Type of Chroma Host - Choose the environment in which your ChromaDB instance is hosted.

Example - Your own ChromaDB server
- Host - Specify the server address to connect to Chroma.

Example - localhost
- Port - Define the port where Chroma is listening.

Example - 8330
- Collection - Set the collection name where your documents will be stored and queried.

Example - ROCKETRIDE

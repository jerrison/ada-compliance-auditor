# Pinecone Vector Store


The Pinecone Vector Store node connects your pipeline to a Pinecone index, enabling high-speed vector search capabilities. It stores and retrieves document embeddings and matches them against queries using vector similarity.


### Inputs


- Documents - Receives vectorized documents to be stored in the Pinecone collection.
- Questions - Accepts vectorized queries for searching similar embeddings in Pinecone.


### Outputs


- Answers - Returns the best-matching vectors or metadata based on the retrieval score.
- Documents - Emits document information retrieved from Pinecone for further use.
- Questions - Forwards the incoming query vector downstream (e.g., into LLMs or logs).


### Configuration Steps


- Type of Pinecone Connection - Choose your Pinecone connection method

Example - Pinecone Pod-Based Index
- API Key - Enter your Pinecone API key
- Retrieval Score - Select the minimum similarity threshold for result relevance

Example - Related
- Collection - Specify the name of the Pinecone collection (index)

Rules - lowercase, alphanumeric, hyphens allowed
Example - rocketride

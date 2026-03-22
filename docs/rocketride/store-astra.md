# Astra DB Vector Store


The Astra DB Vector Store node (astra_db) connects your pipeline to DataStax Astra DB for vector storage and semantic search. It supports both lexical (BM25) and vector-based retrieval, making it suitable for RAG workflows that need hybrid search capabilities.


## Configuration


| Field | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| collection | string | Yes | — | Collection name (alphanumeric and underscores, must start with a letter or digit) |
| api_endpoint | string | Yes | — | Astra DB Data API endpoint URL |
| application_token | string | No | — | Authentication token |
| similarity | string | No | cosine | Vector similarity metric: cosine, euclidean, or dot_product |


## Inputs and Outputs


### Input Channels


- Questions (writeQuestions) — Question objects for semantic or keyword search against the collection.
- Documents (writeDocuments) — Document objects with embeddings for ingestion into the vector store.
- Render Object (renderObject) — Retrieve and stream complete documents by ID.


### Output Channels


- Documents — Search results returned as document objects with similarity scores.
- Text — Rendered document content retrieved via the render object channel.


## Key Details


- Built on the Astra DB Data API using the astrapy package.
- Supports dual search modes: lexical (BM25) and semantic (vector similarity).
- Automatically configures lexical indexes with a standard analyzer.
- Collections are created with both vector and lexical index support.
- Documents are ingested in batches of 500 with automatic flush.
- Zero-magnitude vectors are rejected during ingestion.
- Filters on nodeId, parent, permissions, isDeleted, and chunkId ranges.


## Common Use Cases


- RAG pipelines — Store embeddings and retrieve relevant context for LLM-powered question answering.
- Hybrid search — Combine keyword and semantic search for more accurate retrieval.
- Serverless vector storage — Use Astra DB's serverless infrastructure without managing database clusters.


## Additional Resources


- DataStax Astra DB Documentation
- Astra DB Data API Reference

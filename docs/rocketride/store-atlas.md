# Atlas Vector Store


The Atlas Vector Store node (atlas) connects your pipeline to MongoDB Atlas for vector search and document storage. It leverages Atlas's built-in vector search indexes and text search capabilities to power RAG workflows.


## Configuration


| Field | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| host | string | Yes | — | MongoDB Atlas URI (e.g. mongodb+srv://...) |
| database | string | Yes | — | Database name (max 64 chars, no special characters) |
| collection | string | Yes | — | Collection name (max 120 chars, cannot start with system.) |
| apikey | string | Yes | — | Atlas API key (used for validation) |
| similarity | string | No | cosine | Vector similarity metric: cosine, euclidean, or dotproduct |
| score | float | No | 0.5 | Minimum retrieval score threshold |
| vectorIndexName | string | No | vector_index | Name of the vector search index |
| textIndexName | string | No | text_index | Name of the text search index |
| payloadLimit | integer | No | 32 MB | Maximum payload size in bytes |
| renderChunkSize | integer | No | 32 MB | Chunk size for document rendering |


## Inputs and Outputs


### Input Channels


- Questions (writeQuestions) — Question objects for vector or text search.
- Documents (writeDocuments) — Document objects with embeddings for indexing.


### Output Channels


- Documents — Search results returned as document objects with scores.
- Text — Rendered document content.


## Key Details


- Requires a MongoDB Atlas M10+ cluster or serverless instance for vector search support.
- Automatically creates text indexes on the content field and kNN vector indexes.
- Vector search uses MongoDB aggregation pipelines with numCandidates optimization.
- Text search uses MongoDB full-text search operators.
- Document ingestion uses a delete-then-insert strategy for updates.
- Filters on nodeId, objectId, parent, permissions, isDeleted, and chunkId.
- Powered by the pymongo package.


## Common Use Cases


- RAG with MongoDB — Organizations already using MongoDB Atlas can add vector search without a separate vector database.
- Hybrid search — Combine vector similarity and full-text search for comprehensive retrieval.
- Enterprise document storage — Leverage Atlas's security, compliance, and scaling features.


## Additional Resources


- MongoDB Atlas Vector Search
- MongoDB Atlas Documentation

# Index Search


The Index Search node (index_search) provides a unified search abstraction that supports both Elasticsearch and OpenSearch backends. It can operate in full-text index mode or vector store mode, making it a flexible choice for pipelines that need keyword search, semantic search, or both.


## Configuration


### Common Fields


| Field | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| provider | string | Auto | — | Backend type: elasticsearch or opensearch (auto-detected) |
| collection / index | string | Yes | — | Index name (1–255 chars, lowercase, alphanumeric with ., _, -) |
| mode | string | No | vstore | Operation mode: index (full-text) or vstore (vector) |
| search | boolean | No | false | Enable text search alongside vector search |


### OpenSearch Fields


| Field | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| host | string | Yes | — | OpenSearch host URL |
| dim | integer | Yes (vstore) | — | Vector dimension |
| score | float | No | 0.0 | Minimum score threshold (0–1) |
| auth.enabled | boolean | No | false | Enable basic authentication |
| auth.username | string | No | — | Basic auth username |
| auth.password | string | No | — | Basic auth password |


### Elasticsearch Fields


| Field | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| host | string | Yes | — | Elasticsearch host |
| port | integer | Yes | — | Elasticsearch port (must be > 0) |
| apikey | string | No | — | API key for authentication |


### Search Options (when search is enabled)


| Field | Type | Default | Notes |
| --- | --- | --- | --- |
| matchOperator | string | or | Match mode: and, or, or exact (phrase match) |
| slop | integer | — | Word distance allowed for phrase search |
| highlight | boolean | false | Enable result highlighting |
| fragment_size | integer | 150 | Highlight fragment size in characters |


## Inputs and Outputs


### Input Channels


- Questions (writeQuestions) — Question objects for text or vector search.
- Documents (writeDocuments) — Document objects with embeddings (vector store mode).
- Text (writeText) — Raw text for indexing (index mode).


### Output Channels


- Documents — Search results as document objects with similarity scores.
- Answers — Text search hits with optional highlighting.
- Text — Retrieved text content.


## Operation Modes


### Index Mode (mode: "index")


Full-text search using BM25 scoring. Supports three match operators:


- or — Matches documents containing any of the search terms.
- and — Matches documents containing all search terms.
- exact — Phrase matching with optional slop for word distance tolerance.


### Vector Store Mode (mode: "vstore")


Semantic search using vector similarity:


- OpenSearch — Uses kNN with FAISS engine and configurable space type (based on similarity metric).
- Elasticsearch — Uses kNN with numCandidates optimization.


## Key Details


- Auto-detects whether the backend is Elasticsearch or OpenSearch.
- Automatically creates indexes with proper field mappings for the selected mode.
- Supports highlight extraction with custom HTML markers.
- OpenSearch vector search uses HNSW algorithm via FAISS engine.
- Powered by opensearchpy and elasticsearch packages.


## Common Use Cases


- Enterprise search — Full-text search over indexed documents with BM25 ranking.
- RAG pipelines — Vector store mode for semantic retrieval to feed LLM context.
- Hybrid search — Combine full-text and vector search in a single node.
- Migration flexibility — Switch between Elasticsearch and OpenSearch backends without changing pipeline logic.


## Additional Resources


- Elasticsearch Documentation
- OpenSearch Documentation

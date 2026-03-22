# Vectorizer


The Vectorizer node (vectorizer) is an orchestration node that combines text preprocessing, embedding generation, and vector storage into a single step. Instead of wiring separate preprocessor, embedding, and store nodes, you can configure all three within the Vectorizer to simplify your pipeline.


## Configuration


The Vectorizer wraps three sub-configurations:


| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| preprocessor | nested config | No | Text preprocessing service configuration |
| embedding | nested config | No | Embedding model service configuration |
| store | nested config | No | Vector store backend configuration |


Each nested config follows the same schema as its standalone node counterpart. For example, the embedding config accepts the same fields as whichever embedding node you select (OpenAI, Cohere, etc.).


## Inputs and Outputs


### Input Channels


- Text (writeText) — Raw text to preprocess, embed, and store.
- Table (writeTable) — Table data to vectorize.


### Output Channels


- Documents (writeDocuments) — Document objects with embeddings and metadata (in transform mode).


## Execution Modes


| Mode | Behavior |
| --- | --- |
| Instance | Preprocesses text, generates embeddings, and writes directly to the configured vector store. |
| Transform | Preprocesses text and generates embeddings, then outputs document objects via writeDocuments for downstream nodes to handle storage. |


## Key Details


- Chains preprocessing → embedding → optional storage in a single node.
- Text is chunked by the configured preprocessor before embedding.
- Each chunk gets metadata: chunkId, tableId, isTable, isDeleted, permissionId.
- Respects the VECTORIZE flag on source objects to control which content is vectorized.
- Supports document rendering via callback (retrieves stored documents).
- Multi-provider support — you can mix and match preprocessor, embedding, and store backends.


## Common Use Cases


- Simplified RAG ingestion — Preprocess, embed, and store documents in one node instead of three.
- Pipeline prototyping — Quickly set up a vectorization pipeline without wiring multiple nodes.
- Batch document processing — Ingest large document sets with built-in chunking and embedding.

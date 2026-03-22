# Nodes Overview


Nodes are the building blocks of every RocketRide pipeline. Each node performs a single, well-defined operation — receiving data through input lanes, processing it, and passing results through output lanes. You compose nodes together on the visual canvas to build pipelines of any complexity.


## Node Categories


RocketRide ships with 68 nodes across 14 categories:


### Source (15 nodes)


Where data enters the pipeline. Every pipeline must start with a source node.


- Webhook — Receive data via HTTP requests from external services
- Chat — Interactive conversational interface for real-time messaging
- Dropper — File-based input via drag-and-drop


Plus 12 additional source types for various input methods.


Browse Source nodes →


### LLM (13 nodes)


Language model providers for text generation, chat, and reasoning.


Supported providers include OpenAI, Anthropic, Google Gemini, Mistral, Groq, Ollama, and more. Each LLM node can be used standalone or invoked as a tool by an agent or parent LLM.


Browse LLM nodes →


### Store (9 nodes)


Vector database integrations for storing and querying embeddings.


Supported stores include Pinecone, Qdrant, Weaviate, Milvus, ChromaDB, pgvector, and more. Each store node supports both upsert (write) and query (read) operations.


Browse Store nodes →


### Text (7 nodes)


Text analysis and transformation nodes.


Includes Named Entity Recognition (NER), PII detection and anonymization, sentiment analysis, text classification, summarization, and more.


Browse Text nodes →


### Agentic (4 nodes)


Agent framework orchestration for multi-step, autonomous workflows.


Supports CrewAI and LangChain agent frameworks. Agent nodes can invoke other nodes (LLMs, tools, stores) as part of their reasoning loop.


Browse Agentic nodes →


### Other (4 nodes)


Utility and routing nodes for pipeline control flow.


Includes conditional routing, data merging, and general-purpose utility operations.


Browse Other nodes →


### Embedding (3 nodes)


Generate vector representations of text for use with vector stores.


Supports OpenAI, Cohere, and local embedding models.


Browse Embedding nodes →


### Image (3 nodes)


Image processing nodes including OCR (optical character recognition), image generation, and image analysis.


Browse Image nodes →


### Preprocessor (2 nodes)


Prepare data for downstream processing. Includes text chunking (split documents into manageable pieces) and code processing.


Browse Preprocessor nodes →


### Audio (2 nodes)


Audio transcription and playback. Convert speech to text or generate audio output.


Browse Audio nodes →


### Data (2 nodes)


Document parsing nodes for extracting structured data from files (PDF, DOCX, etc.).


Browse Data nodes →


### Infrastructure (2 nodes)


Output and export nodes for sending pipeline results to external systems.


Browse Infrastructure nodes →


### Video (1 node)


Extract key frames from video files for downstream analysis or processing.


Browse Video nodes →


### Database (1 node)


Direct database access for SQL queries and data retrieval.


Browse Database nodes →


## How Nodes Connect: Lanes


Nodes communicate through lanes — typed connections that carry data between nodes.


- Output lanes emit data from a node after processing.
- Input lanes receive data into a node for processing.


You wire a pipeline by dragging connections from an output lane of one node to a compatible input lane of another on the visual canvas. Lane types ensure that only compatible nodes can be connected.


### Tool Invocation


Some nodes — particularly LLMs and agents — can invoke other nodes as tools. Instead of wiring a direct lane connection, you attach a node as a tool that the parent node can call during its execution. This is commonly used for:


- Giving an LLM access to a vector store for RAG
- Letting an agent call multiple LLMs or APIs
- Building multi-step reasoning chains


## Next Steps


- Quickstart — Build your first pipeline end-to-end.
- Guides — Explore complete pipeline examples.

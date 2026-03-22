# Overview


RocketRide is a high-performance data processing engine built on a C++ core with a Python-extensible node system. With 50+ pipeline nodes, native AI/ML support, and SDKs for TypeScript, Python, and MCP, it lets you process, transform, and analyze data at scale — entirely on your own infrastructure.


## Key Capabilities


- High-performance C++ engine — Native multithreading purpose-built for throughput, not prototypes.
- Visual pipeline builder — Build, debug, test, and scale AI and data workloads from your IDE with an intuitive visual canvas. No browser required.
- 50+ pipeline nodes — Python-extensible, with 13 LLM providers, 8 vector databases, OCR, NER, PII anonymization, and more.
- Multi-agent workflows — Orchestrate and scale agents with built-in support for CrewAI and LangChain.
- TypeScript, Python & MCP SDKs — Integrate pipelines into native applications or expose them as tools for AI assistants.
- One-click deploy — Run on Docker, on-prem, or RocketRide Cloud.


## Core Concepts


### Pipelines


A pipeline is a directed graph of nodes that processes data from input to output. Pipelines are defined as .pipe files (JSON format) and rendered visually in the IDE extension. You can run, monitor, and debug pipelines directly from the canvas.


### Nodes


Nodes are the building blocks of every pipeline. Each node performs a specific operation — calling an LLM, embedding text, querying a vector store, transforming data, and more. Nodes are organized into categories by function:


| Category | Nodes | Description |
| --- | --- | --- |
| Source | 15 | Where data enters the pipeline (webhook, chat, dropper) |
| LLM | 13 | Language model providers (OpenAI, Anthropic, Google, and more) |
| Store | 9 | Vector database integrations (Pinecone, Qdrant, Weaviate, and more) |
| Text | 7 | Text analysis and transformation (NER, PII, sentiment, and more) |
| Agentic | 4 | Agent framework orchestration (CrewAI, LangChain) |
| Other | 4 | Utilities and routing |
| Embedding | 3 | Generate vector representations |
| Image | 3 | Image processing and OCR |
| Preprocessor | 2 | Chunking and code processing |
| Audio | 2 | Transcription and playback |
| Data | 2 | Document parsing |
| Infrastructure | 2 | Output and export |
| Video | 1 | Frame extraction |
| Database | 1 | Direct database access |


For a full breakdown, see the Nodes Overview.


### Lanes


Lanes are the connections between nodes. Each node has typed input lanes and output lanes that define what data it accepts and produces. You wire nodes together by connecting an output lane of one node to a compatible input lane of another. Some nodes (like agents or LLMs) can also be invoked as tools by a parent node.


### Source Types


Every pipeline begins with a source node that defines how data enters:


- Webhook — Receives data via HTTP requests
- Chat — Interactive conversational interface
- Dropper — File-based input via drag-and-drop


## Where to Go Next


- Quickstart — Go from zero to a running pipeline in minutes.
- Guides — Explore pre-built pipelines and common use cases.
- Nodes Overview — Browse all 68 nodes by category.

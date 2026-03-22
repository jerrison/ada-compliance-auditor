# Preprocessor: LLM


An intelligent document preprocessing node that uses Large Language Models to analyze and chunk documents into semantic segments optimized for vector embedding storage and enhanced searchability.



## Key Capabilities


- Intelligent semantic chunking using LLM reasoning to maintain context boundaries
- Table-aware processing that preserves markdown table structure and row integrity
- Automatic document summarization with dedicated summary chunks for overview generation
- Token-aware splitting with configurable limits matching embedding model requirements



## Configuration


### Basic Configuration


- Model Selection: Connect any LLM node via the invoke interface - supports OpenAI, Anthropic, local models, and custom LLM implementations
- numberOfTokens: Configure chunk size to match your embedding model (default 384 tokens)
- LLM Connection: Required minimum 1 LLM connection for document processing operations



## Inputs and Outputs


### Input Channels


- text: Raw text content, accumulated until document processing is complete, no size limit
- table: Markdown table content processed separately with row-boundary preservation


### Output Channels


- documents: Array of Doc objects with DocMetadata including chunkId, objectId, nodeId, parent path, permissions, summary flags, and table indicators



## Supported Model Variants


| Model Variant | Description | Max Tokens | Optimized for |
| --- | --- | --- | --- |
| Any LLM node | Uses invoke interface for universal LLM compatibility | Model-dependent | Document semantic analysis and intelligent chunking |
| OpenAI Models | GPT-3.5, GPT-4 variants via OpenAI node | Model-dependent | High-quality semantic boundary detection |
| Local Models | Ollama, LlamaCpp, and custom local implementations | Model-dependent | Privacy-focused document processing |



## Data Flow Process


1. Text and table inputs accumulate in memory during document processing lifecycle
2. LLM invoked with structured prompt containing chunking guidelines and token limits
3. Response parsed as JSON containing chunks array with content and metadata flags
4. Doc objects created with full metadata including chunkId sequence and summary indicators
5. Documents emitted via writeDocuments() to connected downstream components



## Common Use Cases


- Vector database preparation: Connect text sources → preprocessor:LLM → vector store nodes for RAG applications
- Document analysis pipeline: Wire document extractors → preprocessor:LLM → embedding nodes → search systems
- Content summarization: Use summary chunks from preprocessor:LLM output for document overview generation
- Table processing workflow: Connect structured data sources → preprocessor:LLM table input → document stores with table metadata



## Frequently Asked Questions


Authentication Errors


- LLM invoke failures → Verify connected LLM node configuration and API credentials
- Missing LLM connection → Ensure minimum 1 LLM node is wired to invoke interface


Input Limitations


- Memory issues with large documents → Automatic hierarchical splitting by paragraphs, sentences, then words
- Token limit exceeded → Adjust numberOfTokens parameter to match connected LLM model limits


Response Issues


- Poor chunk quality → Verify LLM model supports structured JSON responses and reasoning
- Empty chunk arrays → Check input text contains chunkable content and LLM response format

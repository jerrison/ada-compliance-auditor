# Ollama


The Ollama node allows users to connect to a locally or remotely hosted Ollama LLM endpoint. It sends natural language prompts to the model and returns generated responses. This is useful for use cases such as summarization, Q&A, and instruction following


### Inputs


- Prompt - Text prompt for the model
- Questions - This port receives the prompt or question to be sent to the LLM. The input must be in plain text format
- Documents - Document objects for context
- System - System instructions for the model


### Outputs


- Text - Generated text output
- Answers - This port outputs the generated text response from the LLM based on the input provided


### Configuration


#### Connection Settings


- Host - Ollama server host

Default - "localhost"
Note - IP address or hostname
- Port - Ollama server port

Default - 11434
Note - Default Ollama API port
- Secure - Use HTTPS connection

Default - false
Note - Set to true for TLS/SSL


#### Model Settings


- Model - Ollama model to use

Default - "llama2"
Note - Any model available in your Ollama installation

Llama2 for general-purpose tasks
CodeLlama for programming tasks
Mistral for high-quality reasoning
Phi-2 for lightweight applications
- Temperature - Creativity/randomness level

Default 0.7
Note - Range: 0.0-1.0
- Max Tokens - Maximum response length

Default - 1024
Note - Limits output size


#### Advanced Settings


- Top P - Nucleus sampling parameter

Default - 0.95
Note - Controls diversity
- Top K - Top-K sampling parameter

Default - 40
Note - Limits token selection
- System Prompt - Default system instructions

Note - Sets model behavior
- Stop Sequences - Sequences to stop generation

Default - []
Note - Custom stop tokens
- Context Window - Maximum context length

Default - 4096
Note - Model-dependent


### Example Usage


Basic Text Generation


This example shows how to configure the Ollama LLM for basic text generation: { "host": "localhost", "port": 11434, "model": "llama2", "temperature": 0.7, "maxTokens": 1024, "topP": 0.95 }


#### RAG Implementation with Mistral Model


For a Retrieval-Augmented Generation (RAG) implementation using the Mistral model: { "host": "localhost", "port": 11434, "model": "mistral", "temperature": 0.3, "maxTokens": 2048, "systemPrompt": "You are a helpful assistant that answers questions based on the provided documents. Always cite your sources and maintain a professional tone.", "topP": 0.9, "contextWindow": 8192 }


Best Practices


#### Resource Management


- Ensure your system has adequate RAM for your chosen model
- Consider quantized models (e.g., Q4_K_M) for reduced memory usage
- Monitor system resources during operation


#### Performance Optimization


- Adjust temperature based on task requirements (lower for factual responses, higher for creative content)
- Set appropriate max tokens to avoid unnecessary processing
- Tune context window size based on your model's capabilities


### Troubleshooting


#### Connection Problems


- Connection refused - Verify Ollama is running and accessible
- Model not found - Ensure the model is downloaded (ollama pull modelname)
- Timeout errors - Check system resources or reduce context size


#### Response Quality Issues


- Irrelevant responses - Refine prompts or adjust system instructions
- Inconsistent outputs - Lower temperature for more deterministic responses
- Truncated responses - Increase max tokens setting or reduce input size


### Technical Reference


For detailed technical information, refer to:


- Ollama Documentation
- Ollama API Reference
- Ollama node Source Code ../../../nodes/llm_ollama/ollama.py

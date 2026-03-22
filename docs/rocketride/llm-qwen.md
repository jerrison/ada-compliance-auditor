# Qwen


The Qwen node (llm_qwen) integrates Alibaba's Qwen large language models via the DashScope API. It uses an OpenAI-compatible endpoint, so it works with standard chat completion interfaces while connecting to Qwen models hosted by Alibaba Cloud.


## Configuration


| Field | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| apikey | string | Yes | — | DashScope API key (must start with sk-) |
| model | string | Yes | — | Qwen model identifier |
| region | string | No | us | Endpoint region: us, intl, or cn |
| modelTotalTokens | integer | No | — | Maximum token limit (must be > 0 if set) |


### Regional Endpoints


| Region | Endpoint |
| --- | --- |
| us | US DashScope endpoint |
| intl | International DashScope endpoint |
| cn | China DashScope endpoint |


## Inputs and Outputs


### Input Channels


- Prompt / Questions — Text prompts or user-generated questions forwarded to the Qwen model.
- Documents — Document objects for additional context.
- System — System instructions for the model.


### Output Channels


- Text / Answers — The model-generated response text.


## Key Details


- Uses the OpenAI-compatible DashScope API, powered by langchain_openai and openai packages.
- Temperature is set to 0 for deterministic outputs.
- API key format is validated during configuration (must start with sk-).
- Includes retry logic with detection of retryable errors (rate limits, transient failures).


## Common Use Cases


- Multilingual workflows — Qwen models have strong multilingual capabilities, especially for Chinese and English tasks.
- Cost-effective inference — Access competitive LLM performance through Alibaba's DashScope platform.
- Regional compliance — Choose between US, international, or China endpoints to meet data residency requirements.


## Additional Resources


- Qwen Model Documentation
- DashScope API Reference

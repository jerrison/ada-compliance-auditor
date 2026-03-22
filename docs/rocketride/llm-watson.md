# IBM Watson


The IBM Watson node (llm_ibm_watson) integrates IBM WatsonX foundation models into your pipeline. It accepts chat prompts, processes them through a selected WatsonX model, and returns generated text. Use this node when your organization runs on IBM Cloud and you want to leverage WatsonX AI models for reasoning, summarization, or content generation.


## Configuration


| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| apikey | string | Yes | IBM Watson API key |
| location | string | Yes | IBM Cloud region (e.g. us-south, eu-de) |
| model | string | Yes | Foundation model ID to use |
| project_id | string | Yes | WatsonX project ID |


All four fields must be provided. The node validates that location is not the placeholder value "Select Location" before connecting.


## Inputs and Outputs


### Input Channels


- Prompt / Questions — Text prompts or user-generated questions forwarded to the WatsonX model for processing.
- Documents — Document objects for additional context.
- System — System instructions for the model.


### Output Channels


- Text / Answers — The model-generated response text.


## Key Details


- Uses the ibm_watsonx_ai Python package to call IBM foundation models.
- Temperature is set to 1.0 for response generation.
- Token estimation uses an approximation of ~0.75 tokens per word.


## Common Use Cases


- Enterprise AI workflows — Organizations on IBM Cloud can keep data and inference within their IBM environment.
- Regulated industries — Leverage WatsonX's compliance and governance features for healthcare, finance, or government use cases.
- Content generation and summarization — Use WatsonX foundation models for document summarization, report generation, and Q&A.


## Additional Resources


- IBM WatsonX AI Documentation
- WatsonX Foundation Models

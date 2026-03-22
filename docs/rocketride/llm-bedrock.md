# Amazon Bedrock


Amazon Bedrock node enables connection to large language models hosted via Amazon Bedrock. This allows users to process questions or text prompts and return generated responses directly in the pipeline.


### Inputs


- Prompt - Text prompt for the model
- Questions - This port receives text-based prompts or questions. It acts as the entry point for sending user or system-generated queries to the LLM
- Documents - Document objects for context
- System - System instructions for the model


### Outputs


- Text - Generated text output
- Answers - This port outputs the model-generated responses. These can be routed to downstream nodes for further processing, display, or storage


### Configuration


#### AWS Authentication


- AWS Access Key - AWS access key ID

Note - Required for authentication
- AWS Secret Key - AWS secret access key

Note - Required for authentication
- AWS Region - AWS region for Bedrock

Default - "us-east-1"
Note - Region where Bedrock is available
- Session Token - AWS session token

Note - Optional, for temporary credentials


#### Model Settings


- Model ID - Bedrock model identifier

Default - "anthropic.claude-3-sonnet-20240229-v1:0"
Note - Available models include Anthropic, AI21, Cohere, etc.

Anthropic Claude models for high-quality reasoning and instruction following
Amazon Titan models for general-purpose tasks
AI21 Jurassic models for complex language understanding
Cohere models for embeddings and semantic search
- Temperature - Creativity/randomness level

Default - 0.7
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
- Timeout - API request timeout

Default - 60
Note - In seconds


### Example Usage


#### Basic Text Generation


This example shows how to configure the Amazon Bedrock LLM for basic text generation: { "awsAccessKey": "your-access-key", "awsSecretKey": "your-secret-key", "awsRegion": "us-east-1", "modelId": "anthropic.claude-3-sonnet-20240229-v1:0", "temperature": 0.7, "maxTokens": 1024, "topP": 0.95 }


#### RAG Implementation with Titan Model


For a Retrieval-Augmented Generation (RAG) implementation using Amazon's Titan model: { "awsAccessKey": "your-access-key", "awsSecretKey": "your-secret-key", "awsRegion": "us-west-2", "modelId": "amazon.titan-text-express-v1", "temperature": 0.3, "maxTokens": 2048, "systemPrompt": "You are a helpful assistant that answers questions based on the provided documents. Always cite your sources and maintain a professional tone.", "topP": 0.9, "timeout": 120 }


### Best Practices


#### AWS Configuration


- Use IAM roles with appropriate permissions when possible
- Store AWS credentials securely
- Consider using temporary credentials with session tokens for enhanced security


#### Performance Optimization


- Adjust temperature based on task requirements (lower for factual responses, higher for creative content)
- Set appropriate max tokens to avoid unnecessary processing
- Choose the AWS region closest to your application for reduced latency


### Troubleshooting


#### AWS Authentication Problems


- Invalid credentials - Verify access key and secret key
- Insufficient permissions - Check IAM policies for Bedrock access
- Region availability - Ensure Bedrock is available in the selected region


#### Response Quality Issues


- Irrelevant responses - Refine prompts or adjust system instructions
- Inconsistent outputs - Lower temperature for more deterministic responses
- Truncated responses - Increase max tokens setting


Technical Reference


For detailed technical information, refer to:


- Amazon Bedrock Documentation
- Bedrock Model IDs
- Bedrock node Source Code ../../../rocketride-nodes/nodes/llm_bedrock/bedrock.py

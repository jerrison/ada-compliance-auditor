# Perplexity


The Perplexity node integrates Perplexity AI's powerful large language models into your RocketRide workflow. This documentation helps you understand how to use and configure the Perplexity node effectively. This is typically used for tasks such as real-time web search, reasoning, content generation, and comprehensive research.


## Key capabilities


- Real-time web search integration
- Context-aware reasoning and analysis
- Comprehensive research capabilities
- Up-to-date information access
- Accurate citations and references


## Configuration


When setting up the Perplexity node, you'll need to configure several parameters:


- Model Selection: Choose the appropriate Perplexity model variant based on your needs
- API Key: Enter your Perplexity AI API key


## Inputs and Outputs


### Input Channels


- Prompt: Primary text input for the model
- Questions: Structured query inputs
- Documents: Text content for additional context
- System: System-level instructions to guide model behavior


### Output Channels


- Text: Generated text responses
- Answers: Structured response outputs with citations


## Supported Model Variants


| Model Variant | Input(s) | Output | Token Limit | Optimized for |
| --- | --- | --- | --- | --- |
| sonar-pro | Text | Text | 127K | High-accuracy search queries |
| sonar | Text | Text | 127K | General search and Q&A |
| sonar-reasoning-pro | Text | Text | 127K | Complex analysis with citations |
| sonar-reasoning | Text | Text | 127K | Standard analytical tasks |
| sonar-deep-research | Text | Text | 127K | Comprehensive research (slower) |
| r1-1776 | Text | Text | 128K | Advanced reasoning, high-quality responses |


## Common Use Cases


- Real-time Information Retrieval
- Access up-to-date information from the web
- Perform fact-checking with citations
- Research current events and trending topics
- Data Analysis
- Extract insights from complex documents with web verification
- Analyze and categorize content with citations
- Generate comprehensive summaries with reference links
- Knowledge-Based Applications
- Build intelligent Q&A systems with real-time search
- Create research assistants with citation capabilities
- Develop tools for comprehensive information gathering



## Frequently Asked Questions


### Authentication Errors


- Invalid API key: Verify PERPLEXITY_API_KEY is set and valid.
- Endpoint unreachable: Confirm PERPLEXITY_API_URL is correct and network-accessible.


### Quality Issues


- Inconsistent responses: Adjust temperature settings or provide clearer instructions.
- Truncated output: Check token limits and adjust max_tokens parameter.



## Additional Resources


- Perplexity AI Documentation
- Perplexity Usage Guides

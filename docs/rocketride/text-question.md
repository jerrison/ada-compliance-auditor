# Question


The Question node is used to define static or dynamic questions that will be paired with text input and sent downstream for answer generation, semantic search, or extraction tasks. This is typically used in Retrieval-Augmented Generation (RAG) pipelines, where predefined questions are evaluated against document content.


## Inputs


- Questions - Question objects to process
- Context - Optional context to enrich questions
- Text - Raw or structured text input that provides the context or content on which the question will operate


## Outputs


- Questions - Emits a question object or string that can be processed further by a vector store, language model (LLM), or answer extraction node


## Configuration


### GUI


- Enter the Question

Fill in the Question field with the query you want to run
Example - What is the customer's account number?


### Question Processing


- Processing Type - Type of question processing

Default - "passthrough"
Options - passthrough, rewrite, decompose, classify
- Language - Language for question processing

Default - "en"
Notes - ISO language code
- Max Length - Maximum question length

Default - 1024
Notes - Characters


## Question Transformation


- Rewrite - Rewrite questions for better retrieval

Default - false
Notes - Improves search quality
- Decomposition - Break complex questions into simpler ones

Default - false
Notes - For multi-part questions
- Classification - Classify question type and intent

Default - false
Notes - For routing to specialized handlers


## Advanced Settings


- LLM Provider - LLM provider for question processing

Default - null
Notes - Required for rewrite, decompose modes
- Custom Templates - Custom prompts for question processing

Default - 
Notes - For specialized question handling
- Caching - Cache processed questions

Default - true
Notes - Improves performance for repeated questions


## Example Usage


### Basic Question Passthrough


This example shows how to configure the Question component for basic passthrough:


{ "processingType": "passthrough", "language": "en", "maxLength": 1024, "caching": true }


### Question Rewriting for Better Retrieval


For rewriting questions to improve retrieval performance:


{ "processingType": "rewrite", "language": "en", "maxLength": 1024, "rewrite": true, "llmProvider": { "provider": "openai", "model": "gpt-4", "temperature": 0.2, "prompt": "Rewrite the following question to make it more specific and detailed for better document retrieval: {question}" }, "caching": true }


### Question Decomposition for Complex Queries


For breaking down complex questions into simpler components:


{ "processingType": "decompose", "language": "en", "maxLength": 1024, "decomposition": true, "llmProvider": { "provider": "openai", "model": "gpt-4", "temperature": 0.3, "prompt": "Break down this complex question into a series of simpler questions that together would help answer the original question: {question}" }, "caching": true }


## Example


- If the Question configured is - "What is the total amount charged?"
- And the input Text is - “Invoice #9283 shows a charge of $450.00 processed on 03/02/2024.”
- The Output would have the answer ready to be used downstream for answering or embedding


## Best Practices


### Question Processing Selection


- Use passthrough for simple, well-formed questions
- Use rewrite for improving retrieval performance
- Use decomposition for complex, multi-part questions
- Use classification for routing questions to specialized handlers
- This node is often the entry point for standardizing questions across multiple documents
- You can connect multiple Text - Question nodes to define several static queries in a pipeline


### Performance Optimization


- Enable caching for applications with repeated questions
- Use custom templates tailored to your domain
- Balance question transformation quality with processing time


## Troubleshooting


### Processing Problems


- Poor rewriting quality - Adjust LLM prompts or try a different model
- Incorrect decomposition - Refine decomposition prompts or adjust temperature
- Misclassified questions - Train on domain-specific examples


### Performance Issues


- Slow processing - Use a faster LLM model or simpler processing type
- High API costs - Optimize caching strategy and LLM usage

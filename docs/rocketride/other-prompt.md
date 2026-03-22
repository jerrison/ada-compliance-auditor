# Prompt


## What does it do?


A node that builds a well-formed prompt from inputs and variables, then emits it for an LLM to execute. The Prompt node acts as a bridge between data sources and language models, enabling template-driven prompt construction with variable substitution, few-shot examples, and output formatting instructions.


## Key Capabilities


Template-driven prompt construction: Build prompts with system/user/assistant sections for structured LLM interactions


Variable substitution and defaulting: Dynamic content insertion with fallback values for missing variables


Few-shot examples and instruction blocks: Include demonstration examples and detailed instructions for better LLM performance


Output shaping: Add instructions and formatting requirements for downstream LLMs



## How do I use it?


### Add the Prompt node


- Insert the node between your data sources and LLM node
- Configure your prompt template with placeholders for variables
- Define default values for optional variables
- Connect input channels for questions and optional documents


### Configure Parameters


The Prompt node focuses on prompt construction only. Model selection, API keys, and LLM-specific settings are configured in the downstream LLM node.


### Configure Input and Output Channels


#### Input Channels


- Documents
- Questions
- Table
- Text


#### Output Channels


- Questions: Rendered prompt as text string, contains the prompt text configured with the context from the inputs.



### Data Flow Process


The Prompt node follows a systematic data processing approach:


#### 1. Input Collection


Action: Collect inputs from questions and optional documents channels


Purpose: Gather all data needed for prompt construction


Process: Read configured template and extract variables from inputs


#### 2. Prompt Rendering


Action: Substitute variables and build complete prompt


Purpose: Transform template and data into executable prompt


Process: Apply variable substitution, attach system instructions, include examples or documents, apply output-format hints


#### 3. Output Emission


Action: Emit single prompt message on questions channel


Purpose: Provide ready-to-execute prompt for LLM consumption


Process: No batching unless pipeline upstream splits inputs



## Common Use Cases


#### Few-shot Prompting


Pipeline: Chain Prompt → LLM


Solution: Provide examples and variables in the Prompt node and send to the LLM node


Result: Enhanced LLM performance through example-based learning


#### RAG Prompting


Pipeline: Vector Store → Prompt → LLM


Solution: Feed retrieved documents into the Prompt node to build context-rich prompts


Result: Knowledge-augmented responses with retrieved context


#### Structured Output Generation


Pipeline: Data Source → Prompt → LLM → JSON Parser


Solution: Include JSON formatting instructions in prompt template


Result: Consistent, structured LLM outputs for downstream processing


#### Dynamic Question Answering


Pipeline: User Input → Prompt → LLM


Solution: Use variable substitution to customize prompts per user query


Result: Personalized responses with consistent prompt structure



## Best Practices


### Template Design


- Use clear variable names with descriptive placeholders
- Define default values for optional variables to prevent errors
- Structure prompts with clear system, user, and assistant sections
- Include specific output format instructions when structured responses are needed


### Variable Management


- Validate required variables are provided in input data
- Use meaningful defaults that won't break downstream processing
- Consider variable length limits for target LLM context windows
- Test with edge cases like empty or very long variable values


### Context Optimization


- Monitor total prompt length to stay within model limits
- Prioritize most relevant documents when context is limited
- Use document chunking strategies for large context requirements
- Include retrieval metadata to help LLM understand document relevance



### Technical Details


### Variable Substitution Process


1. Template Parsing: Identify all variable placeholders in template
2. Input Mapping: Match input data fields to template variables
3. Default Application: Apply configured defaults for missing variables
4. Substitution: Replace placeholders with actual values
5. Validation: Check for any remaining unresolved variables


### Document Integration


- Documents are injected into designated template sections
- Multiple document handling with separators and numbering
- Automatic truncation if context limit is approached
- Metadata preservation for document source tracking


### Error Handling


- Missing required variables trigger structured error outputs
- Template syntax errors are caught during configuration
- Context length violations generate warnings
- Invalid JSON in input data produces descriptive error messages



### Frequently Asked Questions


#### Authentication Errors


Not applicable → API keys are managed by the downstream LLM node.


#### Missing variable in template


Define a default in the template or pass the variable on the questions input.


#### Prompt too large for target model


Reduce included context or chunk upstream before Prompt.


#### Downstream LLM returns unstructured output


Add explicit JSON instructions in the Prompt template and validate downstream.


#### Hallucinations in answers


Strengthen system prompt and include retrieval context via documents input.



### Expected Results


After using the Prompt node in your pipeline:


1. Well-formed Prompts: Consistently structured prompts ready for LLM execution
2. Dynamic Content: Variable substitution enables personalized and context-aware prompts
3. Enhanced Performance: Few-shot examples and clear instructions improve LLM output quality
4. Structured Outputs: Format instructions guide LLMs to produce parseable responses
5. Error Prevention: Validation and defaults prevent downstream processing failures

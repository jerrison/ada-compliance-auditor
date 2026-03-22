# Code


## What does it do?


The Preprocessor - Code node is designed to intelligently parse and tokenize source code files, breaking them down into meaningful components such as functions, classes, and comments. This enables deeper semantic analysis, classification, embedding, or search by preparing code for downstream AI and data processing tasks. The node segments code into logical chunks by detecting syntax boundaries and respecting language-specific structures.


With the Preprocessor - Code node, you can:


- Automatically split code into logical chunks for analysis or embedding
- Extract structural elements (functions, classes, comments) from source files
- Prepare code for advanced AI workflows, such as search, summarization, or classification
- Support multiple programming languages with automatic or manual language selection
- Apply code normalization and formatting for consistent processing
- Remove or preserve comments and docstrings based on your needs



## Inputs and Outputs


### Inputs


- Text – Receives plain code or code-formatted text (raw content to be split and transformed)
- Documents – Document objects containing code to be preprocessed


### Outputs


- Text – Preprocessed code content
- Documents – Emits structured chunks of code as processed document segments (optimized for downstream components such as vector embeddings or LLMs)



## Configuration Fields


### Basic Configuration


| Field | Description | Default | Options/Example | Notes |
| --- | --- | --- | --- | --- |
| Language (Code Splitter Profile) | Programming language to use for parsing | Auto | auto, c, cpp, python, javascript, typescript | Automatically detect or specify manually |
| Maximum String Length | Maximum length (in characters) for each code chunk | - | 512 | Controls chunk size for downstream tasks |


### Code Normalization Options


| Field | Description | Default | Notes |
| --- | --- | --- | --- |
| Remove Comments | Remove code comments | True | Can be configured to preserve docstrings |
| Format Code | Apply code formatting | True | Language-specific formatting rules |
| Remove Whitespace | Normalize whitespace | True | Preserves indentation structure |
| Normalize Identifiers | Standardize variable/function names | False | Useful for code comparison |


### Advanced Settings


| Field | Description | Default | Notes |
| --- | --- | --- | --- |
| Preserve Docstrings | Keep documentation strings | True | Only applies when Remove Comments is True |
| Extract Functions | Extract function definitions | False | Creates separate outputs for each function |
| Extract Classes | Extract class definitions | False | Creates separate outputs for each class |
| Custom Patterns | Apply custom regex patterns | None | For specialized code cleaning |



## How do I use it?


To use the Preprocessor - Code node in your workflow:


1. Add the Preprocessor - Code node

Insert the Preprocessor - Code node into your pipeline where you want to process source code files
2. Connect Input

Connect the input lane (text or documents) to the source of your code
This could be a file dropper, file system, document parser, or any code source
3. Configure Parameters

In the attributes editor, customize how code is processed
Set the programming language (or use "Auto" for automatic detection)
Configure maximum string length for chunk size control
Adjust normalization options based on your needs
4. Connect Output

The node outputs structured code segments (as documents)
Send these to downstream nodes for embedding, search, or further analysis



## Example Use Cases


- Prepare code for semantic search by splitting large files into manageable, meaningful chunks
- Enable code summarization or documentation generation by extracting functions and classes
- Feed code into embedding models for similarity search or clustering
- Automate code review or analysis by breaking down files for AI-powered inspection
- Process code repositories for knowledge base creation
- Normalize code across different projects for comparison and analysis



## Best Practices


### Code Preparation


- Specify the programming language explicitly for best results
- Consider preserving docstrings for documentation-heavy code
- Use function extraction for analyzing specific code components
- Normalize identifiers when comparing code functionality across different implementations


### Performance Considerations


- Code formatting can be resource-intensive for large files
- Processing very large codebases may require batch processing
- Consider memory usage when processing large volumes of code



## Troubleshooting


### Processing Problems


- Incorrect language detection - Specify language explicitly instead of using Auto
- Important comments lost - Enable preserveDocstrings option
- Code structure altered - Disable formatting if precise structure preservation is needed


### Performance Issues


- Slow processing - Disable resource-intensive options like formatting for large codebases
- Memory errors - Process code in smaller batches



## Summary Table of Parameters


| Parameter | Description | Effect/Usage |
| --- | --- | --- |
| Language | Programming language to use for parsing (auto, c, cpp, etc.) | Determines parsing rules and syntax |
| Maximum String Length | Max length (in characters) for each code chunk | Controls chunk size for downstream tasks |
| Remove Comments | Strip comments from code | Cleans code for analysis while optionally preserving docstrings |
| Format Code | Apply language-specific formatting | Standardizes code appearance and structure |
| Extract Functions/Classes | Separate functions and classes into individual outputs | Enables component-level analysis and processing |



In summary:


The Preprocessor - Code node prepares your source code for advanced AI workflows by parsing, chunking, and structuring it for downstream analysis, embedding, or search. It provides comprehensive code normalization and extraction capabilities to optimize code processing for machine learning and AI applications.

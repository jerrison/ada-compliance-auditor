# LlamaParse node


This node uses LlamaParse to extract text and structured data from various document formats including PDFs, images, and other document types.


 



## Features


- Document Parsing: Extracts text content from PDFs, images, and other document formats
- Structured Output: Returns parsed content in markdown format
- Multiple Input Types: Supports both tag-based document streams and document objects


## Input


- Data: Accepts a wide range of file or content types, including binary files, mixed media, or serialized formats


## Outputs


- Text: Outputs extracted text as markdown‑formatted content, preserving headings, lists, and paragraphs where available
- Table: Outputs structured tables extracted from the document (markdown table format)


 



## Configuration


The node supports the following configuration options:


 Required Configuration


- `api_key` (string, optional): Your LlamaParse API key. If not provided, some features may be limited.


### Simple Configuration


- parse_mode (string, default: "cost_effective"): The parsing mode to use for document processing:

 cost_effective (3 cred./page): Best for text-heavy documents without diagrams and images
agentic (10 cred./page): Best for documents with diagrams and images, may struggle with complex layouts
agentic_plus (90 cred./page): Highest parsing setting for complex layouts, multi-page tables, diagrams, and images
parse_page_with_llm (Legacy): Legacy LLM-based parsing mode
parse_page_with_lvm** (Legacy): Legacy LVM-based parsing mode with additional configuration options
lvm_model  (string, optional): The LVM model to use when parse_mode is set to "parse_page_with_lvm", "agentic", or "agentic_plus". Options include "anthropic-sonnet-4.0", "anthropic-sonnet-3.5", "gpt-4o", "gpt-4o-mini".
- `use_system_prompt_append` (boolean, default: false): Whether to add custom instructions to the system prompt.
- `system_prompt_append` (string, optional): Additional instructions to append to the system prompt when use_system_prompt_append is enabled.
- `spreadsheet_extract_sub_tables` (boolean, default: false): Extract sub-tables from spreadsheets for better table parsing.


### Example Configuration


json


```
{  "api_key": "your-llamaparse-api-key-here",  "parse_mode": "agentic",  "use_system_prompt_append": false,  "spreadsheet_extract_sub_tables": false}
```


 



## Parse Mode Selection Guide


- Use cost_effective for:


              • Text-heavy documents (reports, articles, books)


              • Documents without diagrams, charts, or images


              • Budget-conscious processing


- Use agentic for:


              • Documents with diagrams, charts, or images


              • Mixed content documents


              • When you need better visual understanding


- Use agentic_plus for:


              • Complex layouts and multi-page tables


              • Documents with intricate diagrams


              • When maximum accuracy is required


              • Complex technical documents


 



## Error Handling


- If parsing fails, the node returns an empty string and logs the error
- Temporary files are automatically cleaned up after processing
- Thread-safe operations prevent concurrent access issues
- Proper object failure handling with completion codes


 



## Resources


https://www.llamaindex.ai/llamaparse

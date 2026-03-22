# Data Extractor


This component extracts structured data from unstructured or semi-structured text. It identifies and extracts specific fields and values from documents based on configurable extraction rules.


## Use a Data Extractor in a flow


 
To use a Data Extractor in your workflow, follow these steps:


1. Drag the Data Extractor component from the Other section onto your canvas
2. Connect document outputs from upstream nodes to the Documents input
3. Configure the field definitions and extraction settings
4. Connect the output ports to downstream processing nodes


## Inputs


 


| Input | Type | Description |
| --- | --- | --- |
| Documents | Documents | Document objects from which to extract data |
| Text | Text | Raw text content from which to extract data |


## Outputs


 


| Output | Type | Description |
| --- | --- | --- |
| Data | Data | Extracted structured data |
| Documents | Documents | Original documents with extraction metadata added |
| Tables | Tables | Extracted tabular data |


## Configuration


### Field Definitions


 


| Setting | Description | Default | Notes |
| --- | --- | --- | --- |
| Fields | Array of field definitions | [] | Defines the fields to extract |
| Column | Field name/column |  | Required for each field |
| Type | Data type of the field | "string" | Options: string, number, date, boolean |
| Default Value | Default value if extraction fails |  | Optional fallback value |


### Extraction Settings


 


| Setting | Description | Default | Notes |
| --- | --- | --- | --- |
| Extraction Method | Method for data extraction | "llm" | Options: llm, regex, rules |
| LLM Provider | LLM provider for extraction |  | Required if method is "llm" |
| Context Window | Text context size for extraction | 1000 | Characters around potential matches |


### Advanced Settings


 


| Setting | Description | Default | Notes |
| --- | --- | --- | --- |
| Confidence Threshold | Minimum confidence score | 0.7 | For LLM extraction |
| Output Format | Format of extracted data | "json" | Options: json, csv, table |
| Validation | Enable data validation | true | Validates against field types |


## Example Usage


Basic Field Extraction


This example shows how to configure the Data Extractor for basic field extraction:


```
{  "fields": [    {      "column": "invoice_number",      "type": "string",      "defval": ""    },    {      "column": "date",      "type": "date",      "defval": ""    },    {      "column": "total_amount",      "type": "number",      "defval": "0.0"    }  ],  "extractionMethod": "llm",  "contextWindow": 1000,  "confidenceThreshold": 0.7,  "outputFormat": "json",  "validation": true}
```


### LLM-Powered Invoice Extraction


For extracting invoice data using an LLM with specific field definitions:


```
{  "fields": [    {      "column": "invoice_number",      "type": "string",      "defval": ""    },    {      "column": "date",      "type": "date",      "defval": ""    },    {      "column": "due_date",      "type": "date",      "defval": ""    },    {      "column": "vendor_name",      "type": "string",      "defval": ""    },    {      "column": "vendor_address",      "type": "string",      "defval": ""    },    {      "column": "total_amount",      "type": "number",      "defval": "0.0"    },    {      "column": "tax_amount",      "type": "number",      "defval": "0.0"    }  ],  "extractionMethod": "llm",  "llmProvider": {    "provider": "openai",    "model": "gpt-4",    "temperature": 0.2  },  "contextWindow": 2000,  "confidenceThreshold": 0.8,  "outputFormat": "table",  "validation": true}
```


## Best Practices


Field Definition


- Define clear, specific fields with appropriate data types
- Provide default values for optional fields
- Use consistent naming conventions for fields
- Consider the structure of your source documents when defining fields


### Extraction Method Selection


- Use LLM for complex, varied documents requiring understanding
- Use regex for well-defined patterns and simple extractions
- Use rules for structured documents with consistent layouts


### Performance Optimization


- Adjust context window size based on document structure
- Set appropriate confidence threshold based on extraction quality needs
- Enable validation to ensure data quality
- Process documents in batches for large collections


## Troubleshooting


### Common Issues


#### Extraction Problems


- Missing data: Adjust field definitions or try a different extraction method
- Incorrect formats: Check field type definitions or adjust validation rules
- Low confidence scores: Refine LLM prompts or adjust confidence threshold


#### Performance Issues


- Slow processing: Reduce context window size or batch process documents
- Memory errors: Process documents in smaller batches
- High error rates: Validate and refine field definitions

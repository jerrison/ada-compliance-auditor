# Dictionary


The Dictionary node enables lookups, tagging, or transformations using a predefined dictionary structure. It can operate over documents, questions, or general text, and emit structured outputs to be used in retrieval-augmented generation (RAG), classification, or enrichment pipelines.


### Inputs


- Documents - Optional supporting documents for context or reference
- Text- Raw or structured text to process through the dictionary
- Questions/Term - Optional list of user queries for contextual matching or enrichment


### Outputs


- Definitions - Generated term definitions
- Documents - Documents with annotations or tags resulting from dictionary matches
- Answers - Structured answers or matches from the dictionary
- Questions - Processed or enriched questions that may include mapped terms or synonyms


### Configuration


#### Term Extraction


- Extraction Method - Method to identify terms

Default - "auto"
Options - auto, regex, nlp, predefined
- Max Terms - Maximum terms to extract per document

Default - 20
Notes - Limits processing time
- Min Term Length - Minimum character length for terms

Default - 3
Notes - Filters out short terms
- Term Filters - Filters to apply to extracted terms

Default - []
Examples - POS tags, frequency thresholds


#### Definition Generation


- Definition Source - Source for definitions

Default - "context"
Options - context, llm, dictionary, custom
- LLM Provider - LLM provider for definitions

Default - null
Notes - Required if definition source is "llm"
- Context Window - Number of characters around term for context

Default - 500
Notes - For context-based definitions
- Definition Length - Target character length for definitions

Default - 200
Notes - Approximate length guidance


#### Advanced Settings


- Deduplication - Remove duplicate terms

Default - true
Notes - Across all processed documents
- Custom Dictionary - Path to custom dictionary file

Default - null
Notes - For custom definition sources
- Term Grouping - Group related terms

Default - false
Notes - Creates term hierarchies


### Example Usage


### Basic Term Extraction and Definition


This example shows how to configure the Definitions component for basic term extraction and definition:


{ "extractionMethod": "nlp", "maxTerms": 15, "minTermLength": 4, "definitionSource": "context", "contextWindow": 600, "definitionLength": 150, "deduplication": true }


#### LLM-Powered Technical Glossary


For creating a technical glossary using an LLM:


{ "extractionMethod": "nlp", "maxTerms": 30, "minTermLength": 3, "termFilters": [ {"type": "pos", "tags": ["NOUN", "PROPN"]}, {"type": "frequency", "minOccurrences": 2} ], "definitionSource": "llm", "llmProvider": { "provider": "openai", "model": "gpt-4", "temperature": 0.3, "prompt": "Define the following technical term in 1-2 sentences: {term}" }, "definitionLength": 200, "deduplication": true, "termGrouping": true }


### Example


- Input - “Our infrastructure uses Kubernetes and S3.”
- Dictionary - {"Kubernetes": "cloud-native orchestrator", "S3": "Amazon object storage"}
- Output

Answers - Definitions for matched terms
Documents - Original text with terms tagged or explained
Questions - May be rephrased with definitions added for clarity


### Best Practices


#### Term Extraction


- Use NLP-based extraction for technical documents
- Use regex for documents with predictable term patterns
- Apply appropriate filters to reduce noise in extracted terms
- Consider domain-specific term extraction rules


#### Definition Generation


- Use context-based definitions when document contains explanations
- Use LLM-based definitions for technical or specialized terminology
- Provide custom dictionaries for domain-specific terminology
- Adjust context window size based on document structure
- Ensure Dictionary is Configured (Not shown in this screenshot)
- If a UI or configuration file for dictionary terms exists, populate or validate the terms being matched.
- Dictionaries typically consist of key-value pairs, synonyms, or tagged patterns.
- Connect Answers to a downstream QA or retrieval system.
- Connect Documents to a storage or annotation step.
- Connect Questions to LLM or search nodes to enrich prompt quality


### Troubleshooting


#### Extraction Problems


- Too many irrelevant terms - Adjust term filters or increase min term length
- Missing important terms - Try different extraction methods or reduce filters
- Duplicate terms with variations - Enable term grouping


#### Definition Problems


- Definitions too generic - Use domain-specific LLM prompts or custom dictionaries
- Definitions missing context - Increase context window size
- Inconsistent definition quality - Try different definition sources


Technical Reference


For detailed technical information, refer to:


- Definitions API Reference
- Supported NLP Models
- Definitions Source Code ../../../rocketride-nodes/nodes/definitions/definitions.py

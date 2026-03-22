# Named Entity Recognition


The Named Entity Recognition node (ner) extracts named entities from text using HuggingFace transformer models. It identifies people, organizations, locations, dates, and other entity types, then enriches documents with structured entity metadata.


## Configuration


| Field | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| model | string | No | dbmdz/bert-large-cased-finetuned-conll03-english | HuggingFace model ID |
| aggregation_strategy | string | No | simple | Entity aggregation strategy |
| min_confidence | float | No | 0.9 | Minimum confidence threshold for entity filtering |
| store_in_metadata | boolean | No | true | Store extracted entities in document metadata |


### Model Profiles


The default model works well for general English NER. You can substitute any compatible HuggingFace NER model:


| Profile | Model | Best For |
| --- | --- | --- |
| bertLarge | dbmdz/bert-large-cased-finetuned-conll03-english | General English NER (default) |
| bertBase | BERT base NER variant | Faster inference, slightly lower accuracy |
| distilbert | DistilBERT NER variant | Lightweight, fastest inference |
| deberta | DeBERTa NER variant | Higher accuracy on complex text |
| xlmRoberta | XLM-RoBERTa NER | Multilingual entity recognition |
| biomedical | Biomedical NER model | Medical/scientific entity extraction |
| custom | User-specified | Any compatible HuggingFace NER model |


## Inputs and Outputs


### Input Channels


- Text (writeText) — Plain text for entity extraction.
- Documents (writeDocuments) — Document objects to process for entity extraction.


### Output Channels


- Text — Original text passed through.
- Documents — Enriched documents with entity metadata.


## Entity Types


The node extracts the following entity categories (depending on the model):


| Entity Type | Description | Example |
| --- | --- | --- |
| PER | Person names | "John Smith" |
| ORG | Organizations | "OpenAI" |
| LOC | Locations | "San Francisco" |
| MISC | Miscellaneous entities | "Nobel Prize" |
| DATE | Date expressions | "January 2025" |


## Key Details


- Uses the HuggingFace transformers NER pipeline.
- Entities below the min_confidence threshold are filtered out.
- When store_in_metadata is enabled, entities are stored in document metadata keys like entities_per, entities_org, entities_loc, etc.
- Each entity includes: entity_group, word, score, start, and end position.
- Entities are deduplicated and sorted within each type.
- Includes a human-readable entity summary output.


## Common Use Cases


- Document enrichment — Automatically tag documents with people, organizations, and locations for downstream filtering.
- Knowledge graph construction — Extract entities as a first step toward building relationship graphs.
- Compliance and redaction — Identify PII entities (names, locations) for anonymization pipelines.
- Content classification — Use entity distributions to categorize documents by topic or domain.


## Additional Resources


- HuggingFace NER Models
- HuggingFace Transformers Documentation

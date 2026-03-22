# Autopipe


The Autopipe node (autopipe) is a meta-node that dynamically constructs processing pipeline segments based on the current task configuration. Rather than processing data directly, it inspects the pipeline's operation mode and inserts the appropriate filter nodes (parsing, OCR, indexing, vectorization) automatically.


## Configuration


| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| autopipe | nested config | No | Autopipe configuration from the task config |
| store | nested config | No | Vector store config (used in index mode) |


## Inputs and Outputs


Autopipe has no direct input or output lanes. It operates at the pipeline construction level, dynamically inserting filter nodes into the pipeline.


## Operation Modes


| Mode | Behavior |
| --- | --- |
| CONFIG | Passthrough — no filters inserted. |
| SOURCE_INDEX | Passthrough — no filters inserted. |
| INDEX | Inserts a vector store filter and indexer based on the store config. |
| INSTANCE | Inserts parse filter, optional OCR filter (if ocr is enabled), and optional indexer (if index is enabled). |
| TRANSFORM | Inserts parse filter and optional OCR filter (if ocr is enabled). |


## Key Details


- This is an advanced, internal node used for dynamic pipeline construction.
- Dynamically inserts filters using endpoint.insertFilter() at pipeline build time.
- Constructs filter configs with proper IDs, provider references, and input/output lane specifications.
- The filters it inserts are standard nodes (parse, OCR, indexer) — Autopipe just automates their wiring.
- Supports local pipeline building.


## Common Use Cases


- Automated pipeline assembly — Let Autopipe determine which processing stages are needed based on the task type.
- Source ingestion — Automatically add parsing and OCR steps when ingesting documents from a source.
- Index pipelines — Automatically wire vectorization and indexing when building search indexes.


Advanced NodeAutopipe is primarily used internally by the RocketRide pipeline engine. Most users will not need to configure it directly — it is automatically included when the pipeline requires dynamic filter insertion.

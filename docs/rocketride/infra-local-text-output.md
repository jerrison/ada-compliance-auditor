# Local Text Output


The Local Text Output node (local_text_output) writes processed text to the local filesystem. It acts as a sink node — it receives text from upstream nodes and saves it as .txt files in a configured directory. Use this when your pipeline needs to output results to the local machine rather than a network share.


## Configuration


| Field | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| storePath | string | Yes | — | Local output directory path |
| exclude | string | No | N/A | Path prefix to exclude/relativize from source paths |


The exclude field strips a prefix from source file paths to create cleaner relative output paths. When set to N/A or omitted, absolute source paths are used.


## Inputs and Outputs


### Input Channels


- Text (writeText) — Text content to write.


### Output Channels


None — this is a sink node. Text is written to the local filesystem.


## Key Details


- Converts the original source file extension to .txt on output.
- Creates the directory structure matching source paths automatically.
- All files are written with UTF-8 encoding.
- Directories are created with os.makedirs(exist_ok=True).
- Skips writes if no text has been accumulated for a file.
- Logs warnings for path mismatches and I/O errors.


## Common Use Cases


- Local document export — Save processed or extracted text to the local filesystem for review.
- Development and testing — Output pipeline results locally during development without needing network infrastructure.
- Text extraction — Convert documents from various formats to plain text files on disk.

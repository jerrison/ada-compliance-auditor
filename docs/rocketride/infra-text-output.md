# Text Output


The Text Output node (text_output) writes processed text to SMB/CIFS network file shares. It acts as a sink node — it receives text from upstream nodes and writes it to a configured network path. Use this when your pipeline needs to output results to a shared network drive.


## Configuration


| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| server | string | Yes | SMB/network server path |
| targetObjectPath | string | Yes | Network output file path pattern |


## Inputs and Outputs


### Input Channels


- Text (writeText) — Text content to accumulate and write.


### Output Channels


None — this is a sink node. Text is written to the configured network share.


## Key Details


- Outputs to SMB/CIFS network shares (Windows file sharing protocol).
- Appends .txt extension to all output files.
- Maintains the directory structure from source documents.
- All files are written with UTF-8 encoding.
- Caches directory creation to avoid repeated SMB calls.
- Skips empty files (only writes when text has been accumulated).
- Tracks transformation keys (mtime + size) for incremental processing.
- Dependencies: smbclient, smbprotocol.


## Common Use Cases


- Document export — Write processed or summarized text to a shared network drive for team access.
- ETL pipelines — Output extracted and transformed text to network storage as part of a data pipeline.
- Archival — Store pipeline output on network-attached storage for long-term retention.

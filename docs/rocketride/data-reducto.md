# Reducto


The Data–Reducto node utilizes Reducto AI to perform high-quality OCR and parsing on documents, extracting clean text and well-structured tables.


## Input


- Data: Accepts a wide range of file or content types, including binary files, mixed media, or serialized formats


## Outputs


- Text: Outputs extracted text as markdown‑formatted content, preserving headings, lists, and paragraphs where available
- Table: Outputs structured tables extracted from the document (markdown table format)


 



## How to Use


1. Connect a data source to the Data input (example files from the File System, emails, documents)
2. Provide your Reducto API Key in the node configuration
3. Choose a configuration mode:

Simple Mode - Quickly enable parsing options for handwritten text, multilingual documents, or AI-driven summarization
Advanced Mode - Unlock full control over Reducto API parameters by supplying Python dictionaries in the provided fields. This allows fine-tuned parsing behavior beyond the simple options.
4. Use the appropriate output ports (Text and/or Tables) to route the parsed results downstream


 



## Configuration


- API Key (required): Your Reducto API key
- Simple Mode Options:

Contains Handwritten Text – Enables Agentic OCR mode for better handwriting recognition and small text/table cell corrections.
Contains Non-English Text – Enables Multilingual OCR system which can parse non-Germanic languages and unicode symbols.
Enable AI Summarization – Generate a text summary of both tables and figures within your document using AI.
- Advanced Mode:

Provides full access to all Reducto API parameters
Enter Python dictionaries into the fields for Options, Advanced Options, and Experimental Options as documented in the Reducto Parsing Configurations Documentation. This page also contains examples of how to format the options fields.
When Advanced Mode is enabled, any configured settings in the Simple Mode will be ignored


### Notes


- Markdown outputs: Text and Table outputs are emitted as markdown; tables appear in standard markdown table format
- Multiple outputs: A single document can produce both Text and multiple Table outputs


 



## Frequently Asked Questions


- What files can I use? PDFs, images, scanned documents, emails, and other file formats.
- How good is the text recognition? "Agentic" mode offers the best accuracy at a higher cost. "Standard" mode is more economical.


 



## Common Use Cases


- Document Processing: Extract text and data from invoices, receipts, and purchase orders for financial systems integration. Enables automated data entry and reduces manual processing time.
- Research Analysis: Parse scientific papers and research documents to extract key findings and data tables for systematic reviews. Streamlines literature review and meta-analysis processes.
- Contract Analysis: Extract important clauses, dates, and parties from legal documents for compliance verification. Highlights critical terms and conditions automatically.
- Healthcare Documentation: Extract medical information from patient records, laboratory reports, and clinical documents to populate electronic health records. Improves patient care through better data accessibility.


 



### Additional Resources:


Reducto Documentation Reducto API endpoints

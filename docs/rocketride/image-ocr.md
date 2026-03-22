# Image – OCR


The OCR node extracts text from image-based documents or raw images using Optical Character Recognition (OCR). This is useful for converting scanned files, screenshots, or image-based documents into machine-readable text for downstream processing.


### Inputs


- Documents - Accepts structured document-like files (e.g., PDFs or multi-page scans) as input for OCR processing.
- Image - Accepts raw image files (e.g., PNG, JPG) that contain embedded text to be recognized.


### Output


- Text - Emits extracted plain text from either the “Documents” or “Image” input. The output can be used in embedding nodes, LLM prompts, or stored for further analysis


### Configuration Steps


- Type of OCR - Select the OCR mode based on the language structure:

Default - for general mono- or multilingual OCR processing.
- Language - Choose the language that best matches the input text.

Example - English

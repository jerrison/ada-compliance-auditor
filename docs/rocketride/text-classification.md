# Text Classification


This node enables policy-based classification of textual input according to predefined privacy, compliance, or national security categories. It supports multiple classification contexts, including country-specific policies. 


Inputs


- Documents - Document objects to be classified
- Text - Raw or preprocessed text to be classified


### Outputs


- Documents - Document objects with classification metadata added
- Categories - Classification results as category objects
- ClassificationContext - Metadata describing the classification environment or policy scope (example - U.S. Privacy, Germany Data Act)
- Classifications - Detected classification labels matching the input policies (example - SSN, Passport, Sensitive Data)
- Text - Outputs plain text or extracted textual content from documents


### Configuration


#### GUI


1. Select applicable classification policies
The classification interface is organized into three sections:

Selected Classifications - Displays all currently selected policies that will be applied
Custom Classifications - Displays classifications that you have custom built
Predefined Classifications - Pre-built, production-ready policies organized by country and domain
2. Create custom classifications (optional)
Expand the Custom Classifications section and click the Create button to define classification rules specific to your use case.
3. Select predefined classifications
Predefined classifications provide compliance-ready policies that cover common regulatory and privacy frameworks. These save time and reduce errors by offering:

Country-specific regulations (e.g., United States Sensitive Data Policy for HIPAA, SSN, financial data)
Domain-specific standards (e.g., PII detection, financial data, healthcare records)
Regular updates to reflect changing compliance requirements

To apply predefined classifications:

Expand each country or domain section
Check individual policies you want applied to the input
Examples:

United States > Social Security Number (SSN) and Taxpayer ID Policy
Germany > Data Protection Act Classifications
4. Configure output filtering
Note: This filtering option only applies to the Text input/output lane and requires both the Text input and Text output connections to be active.
At the bottom of the configuration panel, choose how to filter the text output:

Match Selected Classifications - Return only text that matches the selected classification policies
Don't Match Selected Classifications - Return only text that does NOT match the selected policies
Return All Text - Return all text regardless of classification matches
5. Review and confirm selections
Verify your selected classifications before proceeding to ensure proper coverage.


##### Note


- All selected policies will be used as context for the classification engine.
- Ensure you only enable policies relevant to your regulatory or operational domain.


Classification Model


- Model Type - Type of classification model

Default - "ml"
Options - ml, rules, hybrid
- Predefined Model - Use a predefined classification model

Default - null
Notes - Available predefined models
- Custom Model Path - Path to custom model file

Default - null
Notes - For user-trained models


#### Classification Categories


- Categories - List of classification categories

Default - []
Notes - Required for rule-based classification
- Hierarchical - Enable hierarchical classification

Default - false
Notes - For nested category structures
- Multi-label - Allow multiple categories per document

Default - false
Notes - For non-exclusive categorization


#### Advanced Settings


- Confidence Threshold - Minimum confidence score

Default - 0.7
Notes - Higher values increase precision
- Feature Extraction - Text feature extraction method

Default - "tfidf"
Options - tfidf, embeddings, custom
- Max Categories - Maximum categories per document

Default - 3
Notes - Only applies when multi-label is true


### Example Usage


### Basic Document Categorization


This example shows how to configure the Document Classification for basic categorization: { "modelType": "ml", "predefinedModel": "general-document-classifier", "confidenceThreshold": 0.7, "multiLabel": false }


#### Custom Classification Rules


For rule-based classification with custom categories: { "modelType": "rules", "categories": [ { "name": "Financial","rules": [ {"type": "keyword", "terms": ["invoice", "payment", "transaction", "bank"]},{"type": "regex", "pattern": "\\$\\d+([.,]\\d{2})"} ] },{ "name": "Legal","rules": [ {"type": "keyword", "terms": ["contract", "agreement", "legal", "law"]},{"type": "regex", "pattern": "section \\d+\\.\\d+"} ] },{ "name": "Technical","rules": [ {"type": "keyword", "terms": ["software", "hardware", "system", "code"]},{"type": "regex", "pattern": "[a-zA-Z0-9_]+\\.[a-zA-Z0-9_]+\\("} ] } ], "hierarchical": false, "multiLabel": true, "maxCategories": 2, "confidenceThreshold": 0.6 }


## Example


- Input Text - “John Doe, SSN: 123-45-6789, lives in California.”
- ClassificationContext - United States
- Classifications - SSN, Personal Data


### Best Practices


#### Model Selection


- Use predefined models for common classification tasks
- Train custom models for domain-specific categorization
- Consider rule-based classification for transparent, explainable results
- Use hybrid approach for complex classification needs


#### Performance Optimization


- Adjust confidence threshold based on precision vs. recall requirements
- Use hierarchical classification for large category sets
- Limit max categories in multi-label mode to improve precision
- Preprocess documents to remove noise that might affect classification


### Troubleshooting


#### Classification Problems


- Low accuracy - Train on more domain-specific data or adjust confidence threshold
- Misclassifications - Review and refine rules or model training data
- No classifications - Check if confidence threshold is too high


#### Performance Issues


- Slow processing - Use a simpler model or feature extraction method
- Memory errors - Process documents in smaller batches


### Technical Reference


For detailed technical information, refer to:


- Document Classification API Reference
- Predefined Classification Models
- Classification Source Code /../../../rocketride-nodes/nodes/classification/classifier.py

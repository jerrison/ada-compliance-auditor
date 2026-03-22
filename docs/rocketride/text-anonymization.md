# Text Anonymization


Text - Anonymize node allows you to anonymize sensitive information from input text using pre-trained named entity recognition (NER) models. It replaces detected entities (like names or organizations) with a specified masking character. 


| Input | Output |
| --- | --- |
| Text - Raw input for anonymization | Text - Anonymized version |
| Classifications - Optional filters |  |


## How It Works


- Scans text for sensitive entities (names, organizations, etc.)
- Model Selection (Choose NER model based on language and domain)
- Replaces detected entities with your chosen masking character (Character used to replace entities, e.g., █ or *))
- Preserves overall text structure while protecting privacy


## **Configuration: **


## Example:


Input: John Smith is a patient at St. Mary's Hospital.


Output: ████ █████ is a patient at ██████████████████.


 


## Tutorial


https://www.youtube.com/watch?v=3IS1rf0Ot4w


## Best Practices:


- Select an appropriate model for your content language and domain
- Use with preprocessor modules for optimal text handling
- Can be integrated into classification pipelines for comprehensive processing

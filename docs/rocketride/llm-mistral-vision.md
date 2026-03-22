# Mistral Vision


The Mistral Vision node integrates Mistral's powerful vision-enabled language models into your workflow. This documentation helps you understand how to use and configure the Mistral Vision node effectively. This is typically used for image analysis, visual reasoning, and generating text responses based on visual inputs.


 


## Key capabilities


- Image-to-text analysis and understanding
- Visual reasoning and problem-solving
- Robust error handling for reliable operation
- Accurate token management
- Support for flexible prompting systems



## Configuration


When setting up the Mistral Vision node, you'll need to configure several parameters: Basic Configuration


- Model Selection: Choose the appropriate Mistral vision model based on your needs
- API Key: Enter your Mistral API key


## Inputs and Outputs


### Input Channels


- Images: Visual inputs in supported formats (PNG, JPEG, GIF, WebP)
- Prompts: Text instructions for the model
- System: System-level instructions to guide model behavior


### Output Channels


- Text: Generated text responses based on image analysis


### Supported Model Variants


| Model Variant | Description | Max Tokens | Optimized for |
| --- | --- | --- | --- |
| pixtral-12b-latest | Pixtral 12B | 4096 | High-performance image understanding |
| pixtral-large-latest | Pixtral Large | 4096 | Best quality image analysis |
| mistral-medium-latest | Mistral Medium | 3025 | Balanced performance and efficiency |
| mistral-small-latest | Mistral Small | 3025 | Fast, efficient image processing |


## Data Flow Process


- Image Accumulation: The system receives image data in chunks and accumulates it
- Question Formation: Images are encoded as base64 data URLs and combined with prompts
- API Communication: Processed data is sent to the Mistral Vision API
- Response Handling: Text responses are returned through the pipeline


## Common Use Cases


### Visual Content Analysis


- Describe and interpret images
- Extract text from images


### Multimodal Reasoning


- Answer questions about visual content
- Generate insights based on images



## Frequently Asked Questions


### Authentication Errors


- Invalid API key: Verify your Mistral API key is set correctly and has vision model access.
- Endpoint unreachable: Confirm network connectivity and API endpoint configuration.


### Input Limitations


- File size: Images must be under 10MB.
- Format support: Only PNG, JPEG, GIF, and WebP formats are supported.


### Response Issues


- Timeout errors: Try with smaller images or simplify your prompt.
- Poor analysis quality: Ensure image clarity and provide more specific prompts.



Additional Resources:


Mistral Vision Mistral Large Model Information Mistral Models on Hugging Face

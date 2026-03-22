# Images


## What does it do?


The Image - Embedding node converts images into high-dimensional vector representations using advanced neural network models. This component generates vector embeddings from images, converting visual content into numerical representations that capture semantic meaning and visual features. These embeddings enable similarity search, clustering, classification, and other AI-powered image analysis tasks.


### Inputs


With the Image - Embedding node, you can:


- Transform images into vectors for use in vector databases or search engines
- Enable image similarity search and content-based retrieval
- Prepare image data for downstream machine learning or AI workflows
- Cluster images by visual similarity for organization or deduplication
- Feed image vectors into AI models for classification or anomaly detection



## Inputs and Outputs


### Inputs


- Images - Image files to convert to embeddings
- Documents - Document objects containing images


### Outputs


- Vectors - Generated vector embeddings
- Documents - Original documents with embeddings attached



## How do I use it?


To use the Image - Embedding node in your workflow:


1. Add the Image - Embedding node

Insert the node into your pipeline where you want to generate embeddings from images
2. Connect Input

Connect the input lane (image or documents) to your image source
This could be a file dropper, file system, image parser, or any image source
3. Configure Parameters

Adjust the embedding model and processing options as needed
Configure image preprocessing settings based on your requirements
4. Connect Output

The node outputs generated image embeddings
Send these to downstream nodes for similarity search, clustering, or further analysis



## Configuration


### Model Settings


| Parameter | Description | Default/Options |
| --- | --- | --- |
| Model | Image embedding model to use | Default: "clip-vit-base-patch32" Available: CLIP, ResNet, EfficientNet |
| Dimensions | Vector dimensions | Default: 512 (model dependent) |
| Batch Size | Number of images to embed at once | Default: 16 (affects memory usage) |
| Normalize | Normalize vector lengths | Default: true (improves similarity calculations) |


#### Available Model Options


- Custom model - User-defined embedding engine, not configured in this view
- Google - 16x16 - Fast, accurate, general-purpose embeddings
- OpenAI - 16x16 - Good performance with lower memory usage
- OpenAI - 32x32 - Lower performance, better image recognition


### Image Processing


| Parameter | Description | Default/Options |
| --- | --- | --- |
| Resize | Resize images before embedding | Default: true (ensures consistent input size) |
| Target Size | Target image dimensions | Default: [224, 224] (width and height in pixels) |
| Center Crop | Apply center cropping | Default: true (maintains aspect ratio) |
| Color Mode | Color processing mode | Default: "RGB" (Options: RGB, grayscale) |


### Advanced Settings


| Parameter | Description | Default/Options |
| --- | --- | --- |
| Cache | Cache embeddings for reuse | Default: true (improves performance for repeated images) |
| Device | Processing device | Default: "auto" (Options: auto, cpu, cuda) |
| Precision | Computation precision | Default: "float32" (Options: float32, float16, bfloat16) |



## Example Use Cases


- Enable reverse image search or "find similar images" features
- Cluster images by visual similarity for organization or deduplication
- Feed image vectors into AI models for classification or anomaly detection
- Build content-based image recommendation systems
- Create visual search engines for e-commerce or media applications
- Perform image quality assessment and analysis
- Enable automated image tagging and categorization



## Best Practices


### Model Selection


- Use CLIP models for general-purpose image embeddings
- Use ResNet models for traditional computer vision tasks
- Use EfficientNet for resource-constrained environments


### Image Preparation


- Ensure consistent image sizes through resizing
- Consider image quality and resolution
- Use center cropping to maintain important visual elements
- Preprocess images to remove noise or irrelevant content


### Performance Optimization


- Adjust batch size based on available memory
- Use GPU acceleration when available
- Enable caching for repeated processing of the same images
- Use lower precision (float16) for faster processing with minimal quality loss



## Troubleshooting


### Processing Problems


- Out of memory errors - Reduce batch size or image dimensions
- Slow processing - Enable GPU acceleration or reduce image size
- Poor embedding quality - Try different models or image preprocessing


### Compatibility Issues


- Model loading errors - Verify model availability and compatibility
- Device errors - Check CUDA installation for GPU acceleration
- Format errors - Ensure images are in supported formats (JPEG, PNG, etc.)



In summary:


The Image - Embedding node transforms images into vector embeddings, enabling powerful AI-driven image search, clustering, and analysis workflows. With comprehensive configuration options for models, preprocessing, and performance optimization, it provides a flexible foundation for image-based AI applications.

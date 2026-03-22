# Image - Thumbnail


## What does it do?


The Image - Thumbnail node automatically generates small, representative thumbnail images from larger image files. These smaller versions of the original images provide quick visual previews, making it easier to browse, display, or organize large collections of images in your workflows. This node is ideal for preparing images for galleries, search results, or any scenario where fast, lightweight image previews are needed.


With the Image - Thumbnail node, you can:


- Create thumbnail previews for images of any size or format
- Standardize image sizes for display in user interfaces or reports
- Speed up image browsing and reduce bandwidth by serving smaller images
- Integrate thumbnail generation into automated data processing pipelines
- Generate visual summaries for reports or pipeline documentation



## Inputs and Outputs


### Input


- Image – Accepts individual image files (e.g., PNG, JPG, JPEG). This is the original content from which the thumbnail will be created.


### Output


- Documents – Outputs the processed image in thumbnail format, typically used as a reference or preview. The result is passed along as a transformed version of the original input image.



## Configuration Fields


The node can be customized to meet your specific thumbnail requirements:


| Parameter | Description | Effect/Usage | Notes |
| --- | --- | --- | --- |
| Thumbnail Size | Set the desired width and height for the generated thumbnails | Controls the dimensions of the output image | Determines preview size and file size |
| Image Format | Choose the output format for thumbnails | Determines file type and compatibility | Options: JPEG, PNG, etc. |
| Quality | Adjust the compression quality for the thumbnails | Balances file size and image clarity | If applicable to chosen format |


Note: In some configurations, no manual setup is required – connecting the image input is sufficient for the node to process and emit thumbnails with default settings.



## How do I use it?


To use the Image - Thumbnail node in your workflow:


1. Add the Image - Thumbnail node

Insert the Image - Thumbnail node into your pipeline where you want to generate thumbnails from images
2. Connect Input

Connect the input lane (image) to the source of your images
This could be a file dropper, file system, image parser, or any image source
3. Configure Parameters (Optional)

In the attributes editor, customize thumbnail generation if needed
Set thumbnail size, image format, and quality based on your requirements
If no configuration is specified, the node will use default settings
4. Connect Output

The node outputs the generated thumbnails as documents
Send these to downstream nodes for display, storage, or further processing



## Pipeline Placement


This node is typically placed:


- After an image ingestion step (file dropper, file system node)
- Before visualization or storage steps
- When previewing data in downstream apps or user interfaces



## Example Use Cases


- Display image previews in web galleries, dashboards, or search results
- Optimize images for faster loading in user interfaces
- Prepare images for machine learning or AI workflows that require standardized input sizes
- Automate thumbnail creation for large batches of images
- Generate visual summaries for reports or documentation
- Create image catalogs or inventories with quick preview capabilities
- Reduce storage and bandwidth requirements for image-heavy applications


https://www.youtube.com/watch?v=SzVMVBg\_2cw



## Best Practices


- Size Selection: Choose thumbnail dimensions that balance preview quality with file size
- Format Choice: Use JPEG for photographs and PNG for images with transparency or sharp edges
- Quality Settings: Adjust compression to find the optimal balance between file size and visual quality
- Pipeline Placement: Position the thumbnail node early in your pipeline to benefit downstream processing



## Summary Table of Parameters


| Parameter | Description | Effect/Usage |
| --- | --- | --- |
| Thumbnail Size | Width and height of the generated thumbnail | Controls the dimensions of the output image |
| Image Format | Output format for the thumbnail (JPEG, PNG, etc.) | Determines file type and compatibility |
| Quality | Compression quality for the thumbnail | Balances file size and image clarity |



In summary:


The Image - Thumbnail node streamlines the creation of image previews, making it easy to generate, display, and manage thumbnails as part of your automated workflows. It provides an efficient way to create standardized image previews that enhance user experience while optimizing performance and storage requirements.

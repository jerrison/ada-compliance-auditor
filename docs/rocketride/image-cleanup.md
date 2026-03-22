# Image Cleanup


## What does it do?


The Image Cleanup node processes images to optimize them for OCR (Optical Character Recognition) tasks by applying a series of automated enhancements. It converts images to grayscale, removes noise, corrects text alignment (deskewing), and enhances contrast to significantly improve OCR accuracy. This is particularly useful for processing low-quality, noisy, or poorly aligned scanned documents and images.



## How do I use it?


### Add the Image Cleanup node


- Insert the node into your pipeline where you want to clean up images
- Typically placed after image sources but before OCR or text extraction components
- Connect it between your image source and downstream processing nodes


### Configure Parameters


The Image Cleanup node uses minimal configuration with these parameters:


| Parameter | Description | Effect/Usage |
| --- | --- | --- |
| No configuration required | The node automatically applies all cleanup steps | Optimizes images for OCR processing |


### Connect Input


- Connect the Image input lane from your image source node
- The node will process each image through the cleanup pipeline
- Supports various image formats (automatically converts to PNG)


### Connect Output


- Connect the Image output lane to downstream components
- Each processed image will be optimized for OCR accuracy
- Output images are in PNG format for consistency



Image Processing Pipeline


The Image Cleanup node applies a four-stage processing pipeline to each image:


#### 1. Format Conversion


Action: Converts all images to PNG format for consistency


Purpose: Ensures uniform processing regardless of input format


Effect: Standardizes image format for downstream processing


#### 2. Binary Conversion


Action: Converts images to grayscale and applies Otsu thresholding


Purpose: Creates clear black and white images for better text recognition


Effect: Reduces noise and improves text contrast


#### 3. Deskewing


Action: Detects and corrects text alignment issues


Purpose: Straightens tilted or rotated text for better OCR accuracy


Effect: Aligns text horizontally for optimal character recognition


#### 4. Morphological Cleanup


Action: Applies morphological closing operations


Purpose: Removes small holes and noise in text characters


Effect: Cleans up character shapes for improved OCR results



Example Use Cases


#### Document Scanning and OCR


Scenario: Processing scanned documents with poor quality or alignment issues


Solution: Use Image Cleanup before OCR to improve text recognition


Result: Higher accuracy OCR results from noisy or misaligned documents


#### Receipt and Form Processing


Scenario: Extracting text from receipts, forms, or handwritten documents


Solution: Clean up images before text extraction


Result: Better recognition of handwritten or printed text


#### Historical Document Digitization


Scenario: Processing old, faded, or damaged documents


Solution: Apply image cleanup to enhance readability


Result: Improved text extraction from degraded documents


#### Mobile Photo Processing


Scenario: Processing photos taken with mobile devices


Solution: Clean up images with varying quality and angles


Result: Consistent text extraction from mobile-captured images



Best Practices


### For Optimal Results


- Place Image Cleanup before OCR components in your pipeline
- Use with various image sources (scanners, cameras, file uploads)
- Combine with other image processing components as needed
- Test with different image qualities to verify improvements


### Pipeline Integration


- Connect after image sources (file system, webhook, etc.)
- Connect before OCR or text extraction components
- Consider using with other image processing nodes
- Monitor processing time for large image batches


### Quality Considerations


- Works best with text-heavy images
- May not be suitable for artistic or graphic-heavy content
- Processing time increases with image size
- Consider image resolution for optimal results



Technical Details


### Processing Steps


1. Format Standardization: Converts all images to PNG format
2. Grayscale Conversion: Reduces color complexity for better processing
3. Noise Reduction: Applies Gaussian blur to reduce image noise
4. Binary Thresholding: Uses Otsu's method for optimal black/white conversion
5. Skew Detection: Analyzes text alignment and calculates rotation angle
6. Image Rotation: Applies calculated rotation to straighten text
7. Morphological Operations: Closes small gaps in text characters
8. Output Generation: Produces cleaned PNG images ready for OCR


### Supported Input Formats


- JPEG/JPG images
- PNG images
- Other common image formats (automatically converted)


### Output Format


- PNG images optimized for OCR processing
- Consistent format for downstream components
- Maintains image quality while improving OCR readiness



Troubleshooting


### Common Issues


- Processing Errors: Check that input images are valid and not corrupted
- Performance Issues: Large images may take longer to process
- Quality Concerns: Very low-quality images may have limited improvement
- Format Issues: Ensure input images are in supported formats


### Performance Considerations


- Processing time scales with image size and complexity
- Consider image resolution for optimal performance
- Batch processing multiple images may require additional time
- Monitor memory usage for large image processing



Expected Results


After using the Image Cleanup node in your pipeline:


1. Improved OCR Accuracy: Better text recognition from cleaned images
2. Consistent Quality: Standardized image format and processing
3. Reduced Noise: Cleaner images with less visual interference
4. Better Alignment: Straightened text for optimal character recognition
5. Enhanced Contrast: Clear black and white images for text extraction


The Image Cleanup node is essential for maximizing OCR accuracy and ensuring reliable text extraction from various image sources, particularly when dealing with low-quality or poorly aligned scanned documents and images.

# Video Key Frame Grabber


Advanced video processing workflow that extracts key frames, generates thumbnails, creates vector embeddings, and stores them in a vector database for similarity search and analysis


- Tutorial
- Overview
- How to Use
- Components
- Pipeline Setup
- Video Formats
- Output Format
- Error Handling
- Performance
- Security



## Tutorial Video




## Pipeline


### Pipeline Components


#### 🌐 Web Hook


Receives uploaded video files via HTTP


#### 📄 Data - Parser


Extracts video content from various file formats


#### 🎬 Video - Frame Grabber


Extracts key frames at specified intervals or scene transitions


#### 🖼️ Image - Thumbnail


Generates optimized thumbnail images


#### 🔍 Embedding - Image


Creates vector embeddings from images using AI models


#### 📊 Vector Store - Qdrant


Stores and retrieves vector embeddings for similarity search



## How to Use the Pipeline


#### Start the Pipeline


1. Log into RocketRide and create a new project
2. Run your pipeline in the RocketRide Engine
3. Look for the Webhook URL message in the Project Log
4. Copy the webhook URL (e.g., http://localhost:8080/webhook/...)


#### Configure API Testing Tool


We recommend using Talend API Tester for easy testing:


- Download: Talend API Tester Extension
- Alternative: Postman, curl, or any HTTP client


#### Set Up the Request


#### Request Configuration


| Field | Value | Description |
| --- | --- | --- |
| Method | PUT | HTTP method for file upload |
| URL | Your webhook URL | The URL from Step 1 |
| Content-Type | Auto | Automatically set based on file type |
| Authorization | Your API key | Found in the webhook URL parameters |


#### Body Configuration


- Type: File
- Upload Method: Drag & drop or click to browse
- Supported Formats: MP4, AVI, MOV, MKV, WebM, and more


#### Send and Process


1. Upload your video file to the request body
2. Click "Send" to submit the request
3. Wait for processing (typically 30-120 seconds depending on video length)
4. Check response status:
✅ 200 OK Success
❌ Error codes Check file format and size



## Component Details


#### 1. Web Hook node


Purpose: Receives HTTP video file uploads and triggers pipeline processing


Configuration:


- Protocol: webhook://
- Class Type: source
- Capabilities: noinclude
- Register: endpoint


Supported Input Types: tags, text, audio, video, image


#### 2. Data - Parser node


Purpose: Extracts structured video content from uploaded files for downstream processing


Configuration:


- Protocol: parse://
- Class Type: data
- Register: filter


Supported Input/Output:


- Input: tags
- Output: text, table, image, video, audio


#### 3. Video - Frame Grabber node


Purpose: Extracts frames from video files at specified intervals, scene transitions, or keyframes


Configuration:


- Protocol: frame_grabber://
- Class Type: video
- Register: filter


#### Frame Extraction Modes


| Mode | Description | Use Case |
| --- | --- | --- |
| Interval | Extract frames at regular time intervals | Consistent sampling |
| Transition | Extract frames at scene changes | Content analysis |
| Keyframe | Extract frames at video keyframes | Compression analysis |


#### Configuration Options


| Setting | Default | Description | Effect |
| --- | --- | --- | --- |
| Percentage Change for Frame | 40% | Scene transition threshold | Lower = more frames at smaller changes |
| Interval Between Frames | 5 seconds | Time between extractions | Controls frame frequency |
| Start Time | 0 seconds | Beginning of extraction | Skips initial video portion |
| Duration | 0 seconds | Extraction duration | Limits processing to segment |
| Maximum Number of Frames | 0 (unlimited) | Frame limit | Stops after reaching limit |


#### 4. Image - Thumbnail node


Purpose: Generates small, representative thumbnail images from larger image files


Configuration:


- Protocol: thumbnail://
- Class Type: image
- Register: filter


Features:


- Aspect Ratio Preservation: Maintains original image proportions
- Optimization: Reduces file size while maintaining quality
- Quick Preview: Enables fast visual browsing
- Storage Efficiency: Reduces storage requirements


#### 5. Embedding - Image node


Purpose: Generates vector embeddings from image content using advanced computer vision models


Configuration:


- Protocol: embedding_image://
- Class Type: embedding
- Capabilities: gpu
- Register: filter


#### Model Options


| Model | Performance | Memory Usage | Use Case |
| --- | --- | --- | --- |
| OpenAI - 16x16 | Good | Lower | General purpose (Default) |
| OpenAI - 32x32 | Lower | Better recognition | High accuracy needed |
| Google - 16x16 | Fast, accurate | General-purpose | Balanced performance |
| Custom Model | Variable | Variable | Hugging Face models |


#### 6. Vector Store - Qdrant node


Purpose: Stores and retrieves vector embeddings for similarity search


Configuration:


- Protocol: qdrant://
- Class Type: store
- Register: filter


#### Host Configuration


| Type | Description | Use Case |
| --- | --- | --- |
| Local | Your own Qdrant server | Development, private deployment |
| Cloud | Qdrant Cloud instance | Production, managed service |



## Configuration Examples


#### Interval-based Frame Extraction


```
Mode: IntervalInterval: 5 secondsStart Time: 0 secondsDuration: 0 (entire video)Max Frames: 0 (unlimited)
```


#### Scene Transition-based Extraction


```
Mode: TransitionPercentage Change: 40%Start Time: 0 secondsDuration: 0 (entire video)Max Frames: 100
```


#### Keyframe-based Extraction


```
Mode: KeyframeStart Time: 0 secondsDuration: 0 (entire video)Max Frames: 50
```



## Supported Video Formats


#### 🎬 Common Video Formats


- MP4 (.mp4) - Most common, good compression
- AVI (.avi) - Windows format, uncompressed
- MOV (.mov) - Apple format, high quality
- MKV (.mkv) - Open source, flexible
- WebM (.webm) - Web-optimized
- MPEG (.mpeg, .mpg) - Legacy format


#### 📏 File Size Recommendations


- Optimal: 10-500 MB
- Maximum: 2 GB
- Processing Time: 30-300 seconds per file


#### ⏱️ Video Length Considerations


- Short Videos (1-5 minutes): 30-60 seconds processing
- Medium Videos (5-15 minutes): 1-3 minutes processing
- Long Videos (15+ minutes): 3-10 minutes processing



## Output Format


### Structured Response


The pipeline outputs multiple types of content:


#### 1. Extracted Frames


Individual video frames as images


#### 2. Thumbnails


Optimized thumbnail versions


#### 3. Vector Embeddings


Numerical representations for similarity search


#### 4. Metadata


Frame timing and extraction information


### Example Output


```
{  "data": {    "objects": {      "cce2fa78-f7fb-5a2e-b391-7c896aeda5cf": {        "text": "FRAMES EXTRACTED:\n- Frame 1: 0.0 seconds\n- Frame 2: 5.0 seconds\n- Frame 3: 10.0 seconds\n\nTHUMBNAILS GENERATED:\n- thumbnail_1.jpg\n- thumbnail_2.jpg\n- thumbnail_3.jpg\n\nEMBEDDINGS CREATED:\n- Vector embeddings for similarity search\n\nSTORED IN QDRANT:\n- Collection: ROCKETRIDE\n- Host: localhost:6333"      }    }  }}
```



## Error Handling


### Common HTTP Status Codes


| Code | Meaning | Solution |
| --- | --- | --- |
| 200 | Success | ✅ Processing completed |
| 400 | Bad Request | Check file format and size |
| 401 | Unauthorized | Verify API key |
| 404 | Not Found | Check webhook URL |
| 500 | Server Error | Restart pipeline |


### Troubleshooting Tips


- File Size: Ensure files are under 2GB
- Format: Use supported video formats
- API Key: Verify authorization header
- Pipeline: Ensure all components are running
- Qdrant Connection: Check vector store configuration
- Network: Check connectivity to webhook endpoint
- GPU: Ensure GPU is available for image embedding models



## Performance Considerations


### Processing Times


| Video Length | File Size | Estimated Time |
| --- | --- | --- |
| 1-5 minutes | 10-100 MB | 30-60 seconds |
| 5-15 minutes | 100-300 MB | 1-3 minutes |
| 15-30 minutes | 300-500 MB | 3-5 minutes |
| 30+ minutes | 500+ MB | 5-10 minutes |


### Optimization Tips


- Video Quality: Use appropriate resolution for your use case

Format Selection: Prefer MP4 for best compatibility
Size Management: Keep files under 500MB for optimal performance
Frame Extraction: Use appropriate intervals to balance detail vs. performance

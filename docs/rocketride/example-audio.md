# Audio Transcription Simple


Streamlined workflow that processes audio files through transcription and summarization with minimal components for maximum efficiency


- Tutorial
- Overview
- How to Use
- Components
- Pipeline Setup
- Audio Formats
- Output Format
- Error Handling
- Performance
- Security



## Tutorial Video




## Pipeline


### Pipeline Components


#### 🌐 Web Hook


Receives uploaded audio files via HTTP


#### 📄 Data - Parser


Extracts audio content from various file formats


#### 🎵 Audio - Transcribe


Converts audio to text using Whisper models


#### 🧠 Text - Summarization: LLM


Creates intelligent summaries using Gemini


#### 📤 HTTP Results


Returns structured JSON output



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
- Supported Formats: MP3, WAV, M4A, FLAC, MP4, AVI, MOV


#### Send and Process


1. Upload your audio file to the request body
2. Click "Send" to submit the request
3. Wait for processing (typically 10-60 seconds depending on audio length)
4. Check response status:
✅ 200 OK Success
❌ Error codes Check file format and size


#### Extract Results


#### Response Structure


```
{  "data": {    "objects": {      "cce2fa78-f7fb-5a2e-b391-7c896aeda5cf": {        "text": "Your processed content here...",        "summaries": [...],        "key_points": [...],        "entities": [...]      }    }  }}
```


#### Extracting Content


1. Open the response JSON
2. Navigate to: data/objects/[object-id]/text
3. Copy the text content - this contains your transcript, summary, key points, and entities
4. Use a simple script to format the output for better readability



## Component Details


#### 1. Web Hook node


Purpose: Receives HTTP audio file uploads and triggers pipeline processing


Configuration:


- Protocol: webhook://
- Class Type: source
- Capabilities: noinclude
- Register: endpoint


Supported Input Types: tags, text, audio, video, image


#### 2. Data - Parser node


Purpose: Extracts structured audio content from uploaded files for downstream processing


Configuration:


- Protocol: parse://
- Class Type: data
- Register: filter


Supported Input/Output:


- Input: tags
- Output: text, table, image, video, audio


#### 3. Audio - Transcribe node


Purpose: Converts audio and video content to text using Whisper models


Configuration:


- Protocol: audio_transcribe://
- Class Type: audio
- Register: filter


#### Model Options


| Model | Speed | Accuracy | Use Case |
| --- | --- | --- | --- |
| Tiny | Fastest | Lowest | Quick processing |
| Base | Fast | Low | General use (Default) |
| Small | Medium | Medium | Balanced |
| Medium | Slow | High | Quality focus |
| Large | Slowest | Highest | Best quality |


#### Advanced Settings


| Setting | Default | Description | Effect |
| --- | --- | --- | --- |
| Silence Threshold | 0.25 seconds | Silence detection threshold | Lower = more sensitive to silence |
| Minimum Seconds | 240 seconds | Minimum audio chunk size | Controls minimum processing batch |
| Maximum Seconds | 300 seconds | Maximum audio buffer size | Controls maximum processing batch |
| VAD Level | Balanced | Voice Activity Detection | Noise filtering aggressiveness |


#### 4. Text - Summarization: LLM node


Purpose: Creates intelligent summaries, key points, and entity extraction using Gemini LLM


Configuration:


- Protocol: summarization://
- Class Type: text
- Register: filter
- Invoke: Requires LLM connection


#### Configuration Options


| Setting | Description | Default |
| --- | --- | --- |
| Number of Summaries | Chunks to summarize after document split | Optional |
| Summary Words | Words per summary (0 = disabled) | Optional |
| Key Point Words | Words per key point (0 = disabled) | Optional |
| Entities | Number of entities to extract (0 = disabled) | Optional |


#### 5. HTTP Results node


Purpose: Returns structured JSON responses with processed content


Configuration:


- Protocol: response://
- Class Type: infrastructure
- Register: filter


Lane Configuration: Text, Audio, Video, Image, Documents, Questions, Answers



## Supported Audio Formats


#### 🎵 Audio Files


- MP3 (.mp3) - Most common, good compression
- WAV (.wav) - Uncompressed, high quality
- M4A (.m4a) - Apple format, good quality
- FLAC (.flac) - Lossless compression
- OGG (.ogg) - Open source format


#### 🎬 Video Files with Audio


- MP4 (.mp4) - Common video format
- AVI (.avi) - Windows video format
- MOV (.mov) - Apple video format
- MKV (.mkv) - Open source video format


#### 📏 File Size Recommendations


- Optimal: 1-50 MB
- Maximum: 100 MB
- Processing Time: 10-60 seconds per file



## Output Format


### Structured Response


The pipeline outputs four types of content:


#### 1. Transcript


The full text transcription of the audio


#### 2. Summary


Condensed version of the content


#### 3. Key Points


Bullet-point summary of main topics


#### 4. Entities


Named entities mentioned in the content


### Example Output


```
{  "data": {    "objects": {      "cce2fa78-f7fb-5a2e-b391-7c896aeda5cf": {        "text": "TRANSCRIPT:\nThis is the full transcript of the audio content...\n\nSUMMARY:\nThis audio discusses the main topics covered in the content...\n\nKEY POINTS:\n• First key point about the content\n• Second key point about the content\n• Third key point about the content\n\nENTITIES:\n• Entity 1: Description\n• Entity 2: Description"      }    }  }}
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


- File Size: Ensure files are under 100MB
- Format: Use supported audio/video formats
- API Key: Verify authorization header
- Pipeline: Ensure all components are running
- LLM Connection: Check LLM configuration and API key
- Network: Check connectivity to webhook endpoint



## Performance Considerations


### Processing Times


| Audio Length | File Size | Estimated Time |
| --- | --- | --- |
| 1-5 minutes | 1-10 MB | 10-30 seconds |
| 5-15 minutes | 10-30 MB | 30-60 seconds |
| 15-30 minutes | 30-50 MB | 1-2 minutes |
| 30+ minutes | 50-100 MB | 2-5 minutes |


### Optimization Tips


- Audio Quality: Use clear, high-quality audio files
- Format Selection: Prefer MP3 or WAV for best compatibility
- Size Management: Keep files under 50MB for optimal performance
- Batch Timing: Allow 30-60 seconds between requests
- Model Selection: Use "Base" model for speed, "Large" for accuracy



## Security and Authentication


### API Key Management


- Location: Found in webhook URL parameters
- Format: Long alphanumeric string
- Security: Keep private and secure


### Request Validation


The pipeline validates:


- File format compatibility
- File size limits
- API key authenticity
- Request method (PUT only)

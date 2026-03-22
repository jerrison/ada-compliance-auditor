# Audio - Transcribe


## What does it do?


The Audio - Transcribe node converts audio or video files into text using advanced speech-to-text models. It provides options to fine-tune silence detection, chunking, and model selection, making it ideal for transcribing interviews, meetings, lectures, or any spoken content.



## How do I use it?


To use the Audio - Transcribe node in your workflow:


1. Add the Audio - Transcribe node

Insert the node into your pipeline where you want to transcribe audio or video files
2. Connect Input

Connect the input lane (usually audio or video) to your audio or video source
3. Configure Parameters

Adjust the transcription model, silence detection, chunking, and VAD level as needed (see tables below)
4. Connect Output

The node outputs the transcribed text for further processing, analysis, or storage



## Configuration Parameters


Customize the transcription process with the following parameters:


| Parameter | Description | Effect/Usage |
| --- | --- | --- |
| Model | The Whisper model to use for transcription (see model options below) | Controls speed and accuracy of transcription; larger models are slower but more accurate |
| Silence Threshold | The silence threshold (in seconds) to detect silence in speech | Lower values are more sensitive to silence; higher values may treat more as speech |
| Minimum Seconds | The minimum seconds of audio to process in a batch and to look for silence | Controls the minimum chunk size for processing |
| Maximum Seconds | The maximum seconds of audio to buffer and process at once | Controls the maximum chunk size for processing |
| VAD Level | Voice Activity Detection (VAD) level for silence detection (see VAD options below) | Controls how aggressively the system filters out non-speech and background noise |



## Model Options


Choose the Whisper model that best balances speed and accuracy for your needs:


| Option | Description | Performance |
| --- | --- | --- |
| tiny | Fastest, least accurate | Quickest processing, basic accuracy |
| base | Fast, low accuracy | Good speed, improved accuracy |
| small | Medium speed and accuracy | Balanced performance |
| medium | Slower, high accuracy | Better accuracy, longer processing |
| large | Slowest, highest accuracy | Best accuracy, longest processing time |


## VAD Level Options


Voice Activity Detection (VAD) controls how the system distinguishes speech from silence and noise:


| Option | Description | Behavior |
| --- | --- | --- |
| Most permissive | Detects the most audio as speech | Risk: includes noise |
| Slightly more aggressive | Skips minor background noise | Filters light background sounds |
| Balanced | Moderate filtering of non-speech | Default in many tools |
| Most aggressive | Filters aggressively | May cut off quiet or short speech |



## Example Use Cases


- Transcribe meeting recordings for searchable notes
- Convert podcasts or interviews into text for analysis
- Generate subtitles or captions for video content
- Create searchable archives of recorded lectures or presentations
- Process customer service calls for quality analysis
- Extract text from voicemails or audio messages
- Prepare audio content for accessibility compliance


https://www.youtube.com/watch?v=Gi-frsA2YY0



## Best Practices


- Model Selection: Use smaller models for quick drafts, larger models for final transcripts
- Audio Quality: Higher quality audio produces better transcription results
- Chunking: Adjust minimum/maximum seconds based on your content type (shorter for conversational, longer for lectures)
- VAD Tuning: Start with balanced VAD and adjust based on your audio environment



In summary:


The Audio - Transcribe node provides flexible, high-quality speech-to-text transcription for audio and video files, with customizable options for model selection, silence detection, chunking, and VAD level to fit a wide range of transcription needs.

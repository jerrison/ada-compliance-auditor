# Video Frame Grabber


## What does it do?


The Video - Frame Grabber node extracts still image frames from video files using one of three selectable modes: at regular intervals, at scene transitions (based on percentage change), or at keyframes. This enables flexible and targeted extraction of representative frames for analysis, preview, or downstream processing.



## How do I use it?


To use the Video - Frame Grabber node in your workflow:


1. Add the Video - Frame Grabber node

Insert the node into your pipeline where you want to extract frames from video files
2. Connect Input

Connect the input lane (usually video) to your video source
3. Configure Parameters

Frame Grabber Mode: Select how frames are extracted:
Interval: Extract frames at regular time intervals
Transition: Extract frames at scene transitions (based on percentage change)
Key: Extract frames at video keyframes
Depending on the selected mode, different parameters will be available (see tables below)
4. Connect Output

The node outputs the extracted image frames for further processing or display



## Frame Extraction Modes


The Video - Frame Grabber offers three distinct modes, each optimized for different use cases:


- Interval Mode: Extracts frames at regular time intervals - ideal for consistent sampling
- Transition Mode: Extracts frames at scene changes - perfect for capturing key moments
- Keyframe Mode: Extracts frames at video keyframes - efficient for video analysis



## Parameters by Mode


### Interval Mode


Extract frames at regular time intervals for consistent sampling throughout the video.


| Parameter | Description | Effect/Usage |
| --- | --- | --- |
| Interval Between Frames | Time in seconds between each extracted frame | Sets frequency of frame extraction |
| Start Time | When to start extracting (in seconds) | Skips initial part of the video |
| Duration | How long to extract frames (in seconds, 0 = end) | Limits extraction to a segment |


### Transition Mode (Scene Change)


Extract frames when significant scene changes are detected based on percentage change threshold.


| Parameter | Description | Effect/Usage |
| --- | --- | --- |
| Percentage Change for Frame | The percentage change in the video to trigger extraction | Sensitivity to scene transitions |
| Start Time | When to start extracting (in seconds) | Skips initial part of the video |
| Duration | How long to extract frames (in seconds, 0 = end) | Limits extraction to a segment |
| Maximum Number of Frames | Cap on frames extracted (0 = unlimited) | Prevents excessive output |


### Keyframe Mode


Extract frames at video keyframes for efficient processing and analysis.


| Parameter | Description | Effect/Usage |
| --- | --- | --- |
| Start Time | When to start extracting (in seconds) | Skips initial part of the video |
| Duration | How long to extract frames (in seconds, 0 = end) | Limits extraction to a segment |
| Maximum Number of Frames | Cap on frames extracted (0 = unlimited) | Prevents excessive output |



## Example Use Cases


- Generate thumbnails or previews at regular intervals for video galleries
- Extract key scenes for content moderation or highlight reels
- Prepare video data for machine learning by sampling at scene changes or keyframes
- Create video summaries or storyboards for content review
- Extract frames for quality control or visual inspection workflows
- Generate training data for computer vision models from video content


https://www.youtube.com/watch?v=SzVMVBg\_2cw



## Mode Selection Guide


- Use Interval Mode when you need consistent, evenly-spaced samples from your video
- Use Transition Mode when you want to capture important scene changes and key moments
- Use Keyframe Mode when you need efficient extraction aligned with video structure



In summary:


The Video - Frame Grabber node provides three flexible modes—interval, scene change, and keyframe—each with its own set of parameters, allowing you to extract video frames in the way that best fits your workflow and analysis requirements.

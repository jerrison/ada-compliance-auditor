# Audio Player


The Audio Player node (audio_player) plays PCM audio data through the system's speakers. It accepts raw audio streams from upstream nodes and outputs them in real time, making it useful for pipelines that generate or process audio (e.g. text-to-speech or audio transformation workflows).


## Configuration


This node has no user-configurable fields. Audio parameters are fixed:


| Parameter | Value |
| --- | --- |
| Sample rate | 44,100 Hz |
| Channels | 2 (stereo) |
| Max chunk size | 16 KB |
| Max queue depth | 32 chunks |


## Inputs and Outputs


### Input Channels


- Audio (writeAudio) — Raw PCM audio data (action, MIME type, buffer bytes).
- Video (writeVideo) — Video data (audio track is routed to the AVI audio handler).


### Output Channels


- Audio playback through system speakers (no data output lanes).


## Key Details


- Accumulates small audio chunks into 16 KB buffers before playback.
- Uses sounddevice.OutputStream with a low-latency callback for real-time playback.
- Thread-safe queue-based buffering that blocks when the queue reaches maximum depth (32 chunks).
- Audio samples are converted to int16 format using NumPy.
- Gracefully terminates playback when the source stream is exhausted.
- May drop the last ~24ms of audio due to callback frame limitations.
- Dependencies: sounddevice, numpy.


## Common Use Cases


- Text-to-speech preview — Listen to TTS output directly in the pipeline without writing files.
- Audio pipeline debugging — Verify audio processing stages produce correct output.
- Real-time audio monitoring — Monitor live audio streams during pipeline execution.

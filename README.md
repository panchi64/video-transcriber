# Video to Text Transcription Script

A Python script that automates the process of extracting audio from video files and transcribing it using OpenAI's Whisper model. This script processes video files locally, making it suitable for handling sensitive or private content.

## Features

- 🎥 Supports multiple video formats (MKV, MP4, AVI, MOV, etc.)
- 🔊 Automatic audio extraction using FFmpeg
- 📝 High-accuracy transcription using Whisper's large model
- 🧹 Automatic cleanup of temporary files
- 📊 Detailed progress logging
- ⚙️ Configurable output directory
- 🛡️ Comprehensive error handling

## Prerequisites

### System Requirements

- Python 3.7 or higher
- FFmpeg installed on your system
- Sufficient disk space for temporary audio files
- Recommended minimum 16GB RAM (for the large Whisper model)
- NVIDIA GPU (optional, but recommended for faster processing)

### Required Python Packages

```bash
pip install openai-whisper
pip install ffmpeg-python
```

### Installing FFmpeg

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

#### On macOS (using Homebrew):
```bash
brew install ffmpeg
```

## Usage

### Basic Usage
```bash
python main.py path/to/your/video.mp4
```

### Specify Output Directory
```bash
python main.py path/to/your/video.mp4 --output-dir /path/to/output
```

### Example
```bash
python main.py lecture.mp4 --output-dir transcripts
```

## Output

The script will create:
1. A temporary WAV file during processing (automatically deleted after completion)
2. A text file containing the transcription, named `[original_video_name]_transcript.txt`

## Script Workflow

1. **Validation**
   - Checks if FFmpeg is installed
   - Verifies input video file exists and is valid
   - Creates output directory if it doesn't exist

2. **Audio Extraction**
   - Extracts audio track from video
   - Converts to WAV format
   - Optimizes audio settings for transcription

3. **Transcription**
   - Loads Whisper's large model
   - Processes audio file
   - Generates text transcription

4. **Cleanup**
   - Saves transcription to text file
   - Removes temporary audio file
   - Logs completion status

## Error Handling

The script includes error handling for common issues:
- Missing FFmpeg installation
- Invalid or corrupted video files
- Insufficient permissions
- Disk space issues
- Memory constraints
- Failed transcription attempts

## Logging

Detailed logging is implemented throughout the process:
- Operation progress updates
- Error messages with debugging information
- Success confirmations
- File paths and processing details

## Performance Considerations

- **Memory Usage**: The large Whisper model requires ~10GB of RAM
- **Processing Time**: Depends on video length and hardware capabilities
- **GPU Acceleration**: Automatically utilized if available
- **Disk Space**: Temporary audio files require additional storage

## Limitations

- Processing speed depends on hardware capabilities
- Large videos may require significant processing time
- Memory usage (up to ~10GB of VRAM or RAM) can be high due to the Whisper large model

## Troubleshooting

### Common Issues and Solutions

1. **FFmpeg not found error**
   - Ensure FFmpeg is installed and in your system PATH
   - Try running `ffmpeg -version` in terminal/command prompt

2. **Memory errors**
   - Close other applications
   - Use a smaller Whisper model by modifying the model size in the script
   - Consider upgrading RAM if issues persist or GPU.

3. **Long processing times**
   - GPU acceleration can significantly improve performance
   - Consider using a smaller Whisper model for faster processing
   - Break large videos into smaller segments

4. **File permission errors**
   - Ensure you have read/write permissions in both input and output directories
   - Run the script with appropriate permissions

## Acknowledgments

- OpenAI for the Whisper model
- FFmpeg team for their excellent media processing tools

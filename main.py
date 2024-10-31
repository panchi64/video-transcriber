#!/usr/bin/env python3
import os
import sys
import subprocess
import whisper
from pathlib import Path
import argparse
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_ffmpeg():
    """Check if ffmpeg is installed on the system."""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


def extract_audio(video_path, output_path):
    """
    Extract audio from video file using ffmpeg.
    Returns the path to the extracted audio file.
    """
    audio_path = output_path / f"{video_path.stem}.wav"

    cmd = [
        'ffmpeg',
        '-i', str(video_path),
        '-vn',  # Disable video
        '-acodec', 'pcm_s16le',  # Audio codec
        '-ar', '16000',  # Sample rate
        '-ac', '1',  # Mono channel
        '-y',  # Overwrite output file if it exists
        str(audio_path)
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"Audio extracted successfully to {audio_path}")
        return audio_path
    except subprocess.CalledProcessError as e:
        logger.error(f"Error extracting audio: {e.stderr.decode()}")
        raise


def transcribe_audio(audio_path, output_path):
    """
    Transcribe audio using OpenAI's Whisper model.
    Uses the largest available model for best accuracy.
    """
    try:
        # Load the largest model
        logger.info("Loading Whisper model (large)...")
        model = whisper.load_model("large")

        logger.info("Starting transcription...")
        result = model.transcribe(str(audio_path))

        transcript_path = output_path / f"{audio_path.stem}_transcript.txt"
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(result["text"])

        logger.info(f"Transcription saved to {transcript_path}")
        return transcript_path

    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        raise


def main():
    parser = argparse.ArgumentParser(description='Transcribe MKV video using Whisper')
    parser.add_argument('video_path', type=str, help='Path to the MKV video file')
    parser.add_argument('--output-dir', type=str, default='output',
                        help='Directory to save the output files (default: output)')

    args = parser.parse_args()
    video_path = Path(args.video_path)
    output_path = Path(args.output_dir)

    if not video_path.exists():
        logger.error(f"Video file not found: {video_path}")
        sys.exit(1)

    output_path.mkdir(parents=True, exist_ok=True)

    if not check_ffmpeg():
        logger.error("ffmpeg is not installed. Please install ffmpeg first.")
        sys.exit(1)

    try:
        logger.info("Extracting audio from video...")
        audio_path = extract_audio(video_path, output_path)

        logger.info("Starting transcription process...")
        transcript_path = transcribe_audio(audio_path, output_path)

        logger.info("Process completed successfully!")
        logger.info(f"Transcript saved to: {transcript_path}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)

    finally:
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)
            logger.info("Cleaned up temporary audio file")


if __name__ == "__main__":
    main()
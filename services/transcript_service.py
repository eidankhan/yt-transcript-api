from yt_dlp import YoutubeDL
import os
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import timedelta
from utils.transcript_utils import format_timestamp, format_transcript, get_transcript_with_ytdlp
from db.transcript_repository import find_transcript, save_transcript
from models.transcript_model import format_transcript_payload

class TranscriptService:

    def get_transcript(self, video_id: str) -> dict:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)

        lines = []
        for idx, snippet in enumerate(transcript.snippets, start=1):
            start_time = format_timestamp(snippet.start)
            end_time = format_timestamp(snippet.start + snippet.duration)
            lines.append(f"{idx}\n{start_time} --> {end_time}\n{snippet.text}\n")

        data = format_transcript(transcript)
        return {
                "video_id": video_id,
                "language": transcript.language,
                "language_code": transcript.language_code, 
                "transcript": data,
                "transcript_with_timestamps": "\n".join(lines)
            }

    def get_transcript_with_youtubedlp(self, video_id: str, language: str = "en", subtitle_format: str = "srt") -> dict:
        existing = find_transcript(video_id)
        if existing:
            return existing

        raw_data = get_transcript_with_ytdlp(video_id, language, subtitle_format)
        formatted = format_transcript_payload(
            video_id=video_id,
            language=language,
            transcript=raw_data["transcript"],
            transcript_with_timestamps=raw_data["transcript_with_timestamps"],
            metadata=raw_data.get("metadata", {}),
            source="yt-dlp"
        )
        save_transcript(formatted)
        return formatted
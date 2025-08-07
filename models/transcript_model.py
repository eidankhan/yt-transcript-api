from datetime import datetime

def format_transcript_payload(video_id: str, language: str, transcript: str, transcript_with_timestamps: str, metadata: dict = None, source: str = "yt-dlp") -> dict:
    return {
        "video_id": video_id,
        "language": language,
        "transcript": transcript,
        "transcript_with_timestamps": transcript_with_timestamps,
        "metadata": metadata or {},
        "source": source,
        "fetched_at": datetime.utcnow().isoformat()
    }

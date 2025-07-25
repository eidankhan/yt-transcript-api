from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi
import os

class TranscriptService:

    def get_transcript_with_youtube_transcript_api(self, video_id: str, language: str = "en") -> dict:
        """
        Use the YouTube Transcript API to get the transcript of a video. Return the cleaned transcript as string,
        and the raw transcript as a list of dictionaries with timestamps, duration, and text.

        The method does not use the yt-dlp library, but the YouTube Transcript API. Correspondingly, the method does not have access to the video metadata.
        """
        try:
            api = YouTubeTranscriptApi()
            transcript = api.fetch(video_id, languages=[language])
            raw_transcript = transcript.to_raw_data()

            cleaned_transcript = '\n'.join([item['text'] for item in raw_transcript])  # `cleaned_transcript` looks like "Line1\nLine2..."

            return {
                'video_id': video_id, 
                'language': language, 
                'transcript': cleaned_transcript,
                'transcript_with_timestamps': raw_transcript,
            }
            
        except Exception as e:
            raise ValueError(f"youtube_transcript_api error: {str(e)}")

    def get_transcript_with_ytdlp(self, video_id: str, language: str = "en", subtitle_format: str = "vtt") -> dict:

        url = f"https://www.youtube.com/watch?v={video_id}"
        output_path = f"/tmp/{video_id}.%(ext)s"

        ydl_opts = {
            'skip_download': True,
            'writeautomaticsub': True,
            'subtitleslangs': [language],
            'subtitlesformat': subtitle_format,
            'outtmpl': output_path,
            'quiet': True,
            'cookiefile': 'cookies.txt'  # ✅ Required to bypass CAPTCHA
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            subtitle_file = f"/tmp/{video_id}.{language}.{subtitle_format}"

            if not os.path.exists(subtitle_file):
                raise ValueError(f"No transcript file found for language '{language}' in format '{subtitle_format}'.")

            with open(subtitle_file, 'r', encoding='utf-8') as f:
                content = f.read()

            if subtitle_format == "srt":
                clean_text = self._parse_srt(content)
            else:
                clean_text = self._parse_vtt(content)
            return {
                "transcript": clean_text,
                "transcript_with_timestamps": content,
                "metadata": self.get_video_metadata(video_id)
            }
        except Exception as e:
            raise ValueError(f"yt-dlp error: {str(e)}")

    def _parse_srt(self, srt: str) -> str:
        lines = srt.splitlines()
        transcript_lines = []
        for line in lines:
            line = line.strip()
            if (
                line == "" or
                line.isdigit() or
                "-->" in line  # timestamp lines
            ):
                continue
            transcript_lines.append(line)
        return "\n".join(transcript_lines)

    def _parse_vtt(self, vtt: str) -> str:
        lines = vtt.splitlines()
        transcript_lines = []
        for line in lines:
            line = line.strip()
            if line == "" or "-->" in line or line.startswith("WEBVTT"):
                continue
            transcript_lines.append(line)
        return " ".join(transcript_lines)

    def get_video_metadata(self, video_id: str) -> dict:
        """Fetch basic metadata like title using yt-dlp"""
        url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'forcejson': True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    "video_id": video_id,
                    "title": info.get("title"),
                    "uploader": info.get("uploader"),
                    "duration": info.get("duration"),  # in seconds
                    "thumbnail": info.get("thumbnail")
                }
        except Exception as e:
            raise ValueError(f"yt-dlp metadata error: {str(e)}")

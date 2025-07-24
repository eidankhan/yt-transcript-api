from yt_dlp import YoutubeDL
import os

class TranscriptService:

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
            'cookiefile': 'www.youtube.com_cookies.txt'  # ✅ Required to bypass CAPTCHA
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

# transcript_utils.py

from datetime import timedelta
import re

def format_timestamp(seconds: float) -> str:
    """Converts seconds into SRT-style timestamp format."""
    ms = int((seconds - int(seconds)) * 1000)
    t = str(timedelta(seconds=int(seconds)))
    h, m, s = t.split(':')
    return f"{int(h):02}:{int(m):02}:{int(s):02},{ms:03}"

def format_transcript(transcript) -> str:
        raw_text = ' '.join(snippet.text for snippet in transcript.snippets)
        # Remove all characters except letters, spaces, and . ! ?
        cleaned_text = re.sub(r'[^a-zA-Z\s.!?]', '', raw_text)
        # Normalize whitespace
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        return cleaned_text

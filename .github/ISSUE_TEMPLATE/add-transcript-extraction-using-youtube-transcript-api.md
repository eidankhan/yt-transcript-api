---
name: Add transcript extraction using youtube-transcript-api
about: This will serve as a lightweight alternative to `yt-dlp`, avoiding cookie/authentication
  issues.
title: Add transcript extraction using youtube-transcript-api
labels: enhancement, good first issue, help wanted
assignees: eidankhan

---

We want to build a simple feature that fetches the transcript of a YouTube video using the [`youtube-transcript-api`](https://pypi.org/project/youtube-transcript-api/) library and returns it via a Flask API.

## ✅ Goals
- Use `youtube-transcript-api` to fetch the transcript for a given YouTube `video_id`
- Return both:
  - `transcript`: plain text without timestamps
  - `transcript_with_timestamps`: full list of segments
- Integrate this feature inside a Flask route `/transcript/<video_id>`

## 🛠️ Suggested Implementation
A new function can be added in a separate module like `transcript_service.py`, with error handling for cases like:
- Transcripts disabled
- No transcript found
- Invalid video ID

Flask route should call this method and return JSON.

## 📂 Example Output
```json
{
  "video_id": "vJefOB8kec8",
  "language": "en",
  "transcript": "Line 1\nLine 2...",
  "transcript_with_timestamps": [
    { "text": "Line 1", "start": 0.0, "duration": 2.0 },
    { "text": "Line 2", "start": 2.0, "duration": 3.5 }
  ]
}
```

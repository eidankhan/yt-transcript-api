# YouTube Transcript API

This is a Flask-based REST API service designed to fetch YouTube video transcripts. It serves as a backend for projects needing transcript extraction, such as Chrome extensions or other frontend apps.

---

## Features

- Extracts transcript text from YouTube videos by VIDEO_ID
- Returns clean, plain-text transcripts via JSON API
- Handles common errors like unavailable videos or disabled transcripts
- CORS enabled for easy frontend integration

---
> # Complete Step-by-Step Guide: Setup + Git + GitHub Push

## 1. Create Project Directory & Subdirectories

```bash
mkdir "yt-transcript-api"
```


## 2. Set Up Flask Backend in `yt-transcript-api/`

```bash
cd yt-transcript-api
```

## 3. Create `app.py`

Create a file named `app.py` with this content:

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({"message": "YT Transcript API is running with Docker Compose!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

## 4. Create `requirements.txt`

Create `requirements.txt` with:

```
flask==2.3.3
```

## 5. Create `docker-compose.yml`

Create `docker-compose.yml` with:

```yaml
version: "3.9"

services:
  backend:
    image: python:3.11.9-slim
    container_name: flask-backend
    working_dir: /app
    volumes:
      - .:/app
    ports:
      - "5000:5000"
    command: >
      sh -c "pip install --upgrade pip &&
             pip install -r requirements.txt &&
             python app.py"
```

## 6. (Optional) Create `.dockerignore`

Create `.dockerignore`:

```
__pycache__/
*.pyc
*.pyo
*.pyd
venv/
.env
```

## 7. Test Docker Compose (Optional)

Run backend with:

```bash
docker-compose up
```

Visit [http://localhost:5000](http://localhost:5000) to check it runs.

---
> # Transcript Fetching API with yt-dlp

This API endpoint fetches YouTube video transcripts using `yt-dlp`, downloading automatic subtitles (if available) in `.vtt` or `.srt` format. It returns:

* A **clean transcript** with all timestamps and formatting removed, suitable for easy reading or AI summarization.
* The **full transcript with timestamps** (raw subtitle content), useful for syncing notes or displaying subtitles alongside video.

## Implementation Details

### 1. Dependency Management with Docker

* We use a **Dockerfile** to build the backend image.
* The Dockerfile installs:

  * `yt-dlp` Python package via `requirements.txt`
  * System dependencies like `ffmpeg` via `apt-get` to enable subtitle processing.

This ensures consistent environment and all required libraries are available inside the container.

### 2. TranscriptService Method

* `get_transcript_with_ytdlp(video_id, language='en', subtitle_format='vtt')`:

  * Downloads subtitles for the given YouTube video ID.
  * Supports subtitle formats: `vtt` (default) and `srt`.
  * Parses subtitle files to return both:
    * Clean transcript text without timestamps/tags.
    * Raw subtitle content with timestamps.

### 3. Flask API Endpoint

* **Route:** `GET /transcript/<video_id>?lang=en&format=vtt`
* **Query Params:**
  * `lang` (optional) — language code (default: `en`)
  * `format` (optional) — subtitle format, `vtt` or `srt` (default: `vtt`)
* **Response:**

```json
{
  "language": "en",
  "metadata": {
    "title": "Sample YouTube Title",
    "video_id": "abcd1234"
  },
  "transcript": "Line one...\nLine two...",
  "transcript_with_timestamps": "00:00:01 --> 00:00:03\nHello world...",
  "video_id": "abcd1234"
}
```

## How to Use

1. **Build and start backend container with Docker Compose:**

```bash
docker-compose build
docker-compose up
```

2. **Call API endpoint:**

```http
GET http://localhost:5000/transcript/OnLmDObu23Y?lang=en&format=srt
```

3. **Handle response:**

* Use `"transcript"` for clean text.
* Use `"transcript_with_timestamps"` for synced display or advanced processing.

## Notes

> * The Dockerfile installs `ffmpeg`, required for yt-dlp to process subtitles.
> * If subtitles are not available for the video or language, API returns a 400 error with a descriptive message.
> * This API serves as a fallback method when other transcript fetching methods fail.

## 🎯 New Feature: Transcript Fetching via `youtube-transcript-api`

We now support extracting YouTube video transcripts using the [`youtube-transcript-api`](https://pypi.org/project/youtube-transcript-api/) library as a modern and stable fallback to `yt-dlp`. This allows us to retrieve captions without requiring cookies, browser emulation, or downloads.

### ✅ Endpoint

```
GET /transcript/<video_id>
```

#### 🔄 Query Parameters

* None (defaults to auto-detected English transcript)

---

### 📥 Sample Request

```
GET http://localhost:5000/transcript/vJefOB8kec8
```

### 📤 Sample JSON Response

```json
{
  "video_id": "vJefOB8kec8",
  "language": "English",
  "language_code": "en",
  "transcript": "Hello friends Welcome to AI Lets begin...",
  "transcript_with_timestamps": "1\n00:00:00,000 --> 00:00:01,500\nHello, friends!\n\n2\n00:00:01,500 --> 00:00:03,000\nWelcome to AI.\n..."
}
```

### 🧠 How It Works

1. `YouTubeTranscriptApi().fetch(video_id)` fetches a list of subtitle snippets.
2. The `transcript_utils.py` module:
   * Converts each snippet into SRT-style timestamped blocks.
   * Formats plain transcript by:
     * Removing non-alphabetic characters (except `. ! ?`)
     * Normalizing whitespace
3. The API returns both:
   * `"transcript"`: Clean text only (AI-ready)
   * `"transcript_with_timestamps"`: Timestamped for SRT/subtitle usage
### 🛠 Code Structure

* `transcript_utils.py`

  * `format_timestamp(seconds)`: Converts seconds to `HH:MM:SS,mmm`
  * `format_transcript(transcript)`: Joins and sanitizes text

* `TranscriptService.get_transcript(video_id)`

  * Constructs and returns the final API response

* `transcript_controller.py`

  * Defines `GET /transcript/<video_id>` route and handles errors

---

### 📦 Dependencies

Be sure `youtube-transcript-api` is listed in your `requirements.txt`:

```
youtube-transcript-api
```


## 🆕 MongoDB Integration

### 📌 Why We Added It
Previously, transcripts were fetched on-demand using `yt-dlp` or `youtube-transcript-api`, which meant:
- Repeated API calls for the same video
- No persistent storage for analytics or reuse
- Slower response times for frequently accessed transcripts

To solve this, we integrated MongoDB as a lightweight, flexible database to cache and persist transcripts.

### 🛠 What It Does
- Stores each transcript as a document in the `transcript_db.transcripts` collection.
- Automatically checks the database before fetching from YouTube.
- Saves transcripts with metadata including:
  - `video_id`
  - `language`
  - `transcript` (clean text)
  - `transcript_with_timestamps` (SRT/VTT format)
  - `metadata` (title, uploader, duration, thumbnail)
  - `source` (yt-dlp or youtube-transcript-api)
  - `fetched_at` timestamp


### ✅ Benefits
- ⚡ **Faster API responses** for previously requested videos
- 📊 **Persistent storage** for analytics, search, or export
- 🔁 **Reduced load** on YouTube and transcript libraries
- 🧩 **Modular architecture** for future enhancements like TTL caching, keyword search, or user tagging
- 🧭 **MongoDB Compass support** for visual inspection and debugging

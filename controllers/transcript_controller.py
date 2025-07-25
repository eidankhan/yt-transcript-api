from flask import Blueprint, jsonify, request
from services.transcript_service import TranscriptService

transcript_bp = Blueprint("transcript", __name__, url_prefix="/transcript")
transcript_service = TranscriptService()

# @transcript_bp.route("/<video_id>", methods=["GET"])
# def get_transcript_fallback(video_id):
#     language = request.args.get("lang", "en")
#     subtitle_format = request.args.get("format", "vtt")  # 'srt' or 'vtt'

#     try:
#         transcripts = transcript_service.get_transcript_with_ytdlp(video_id, language, subtitle_format)
#         return jsonify({
#             "video_id": video_id,
#             "language": language,
#             "transcript": transcripts["transcript"],
#             "transcript_with_timestamps": transcripts["transcript_with_timestamps"],
#             "metadata": transcripts["metadata"]
#         })
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400

@transcript_bp.route('/<video_id>', methods=['GET'])
def get_transcript_with_youtube_transcript_api(video_id):
    language = request.args.get("lang", "en")
    try:
        transcripts = transcript_service.get_transcript_with_youtube_transcript_api(video_id, language)
        return jsonify({
            "video_id": video_id,
            "language": language,
            "transcript": transcripts["transcript"],
            "transcript_with_timestamps": transcripts["transcript_with_timestamps"],
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
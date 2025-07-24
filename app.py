from flask import Flask
from flask_cors import CORS
from controllers.transcript_controller import transcript_bp
import os

app = Flask(__name__)
CORS(app)  # ✅ This enables CORS for all routes
app.register_blueprint(transcript_bp)  # No need for url_prefix here anymore

# Ensure the cookies file is in the correct location
print("cookies.txt exists:", os.path.exists('cookies.txt'))

@app.route("/")
def home():
    return {"message": "TubeNote AI backend running with Docker Compose!"}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

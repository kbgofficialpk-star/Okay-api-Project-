from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "KBG API SERVER IS ONLINE"

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Best options for fast extraction
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # URL extraction logic
            real_url = info.get('url')
            if not real_url and 'entries' in info:
                real_url = info['entries'][0]['url']

            if not real_url:
                return jsonify({"error": "Link not found"}), 404

            return jsonify({
                "url": real_url,
                "status": "success"
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Using port 5000 which is more stable on Replit
    app.run(host='0.0.0.0', port=5000)
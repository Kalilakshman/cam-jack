from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import os
import datetime

app = Flask(__name__)
CORS(app)

SAVE_DIR = "captures"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    try:
        data = request.get_json()
        image_data = data.get("image", "")

        if "," in image_data:
            image_data = image_data.split(",")[1]

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = os.path.join(SAVE_DIR, f"capture_{timestamp}.png")

        with open(filename, "wb") as f:
            f.write(base64.b64decode(image_data))

        print(f"[+] Saved: {filename}")
        return jsonify({"status": "ok", "file": filename}), 200

    except Exception as e:
        print(f"[!] Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/captures")
def list_captures():
    try:
        files = os.listdir(SAVE_DIR)
        files = [f for f in files if f.endswith(".png")]
        files.sort(reverse=True)

        html = """
        <!DOCTYPE html>
        <html>
        <head>
          <title>Captures</title>
          <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
              background: #0f172a;
              color: #e2e8f0;
              font-family: 'Segoe UI', sans-serif;
              padding: 30px;
              min-height: 100vh;
            }
            h2 {
              font-size: 22px;
              font-weight: 600;
              margin-bottom: 8px;
              color: #94a3b8;
            }
            .count {
              font-size: 13px;
              color: #475569;
              margin-bottom: 24px;
            }
            .grid {
              display: flex;
              flex-wrap: wrap;
              gap: 16px;
            }
            .card {
              background: #1e293b;
              border-radius: 10px;
              overflow: hidden;
              width: 300px;
              border: 1px solid #334155;
            }
            .card img { width: 100%; display: block; }
            .card .label {
              padding: 8px 12px;
              font-size: 11px;
              color: #64748b;
              word-break: break-all;
            }
            .empty {
              color: #475569;
              font-size: 15px;
              margin-top: 60px;
              text-align: center;
              width: 100%;
            }
          </style>
        </head>
        <body>
          <h2>Captured Images</h2>
        """

        html += f"<p class='count'>{len(files)} image(s) captured</p>"
        html += "<div class='grid'>"

        if files:
            for f in files:
                html += f"""
                <div class='card'>
                  <img src='/captures/{f}' alt='{f}' loading='lazy'/>
                  <div class='label'>{f}</div>
                </div>
                """
        else:
            html += "<p class='empty'>No captures yet.</p>"

        html += "</div></body></html>"
        return html

    except Exception as e:
        return f"Error: {e}", 500


@app.route("/captures/<filename>")
def get_capture(filename):
    return send_from_directory(SAVE_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

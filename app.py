from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session
    )
from downloader import downloader as ytd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/process_form", methods=["POST"])
def process_form():
        
    link = request.form["v_link"]
    quality = request.form["res"]
    audio_mode = request.form["a_check"]
    ytd(
        link,
        quality,
        audio_mode
    )
    return redirect(url_for("index"))
if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0',port=5000)

# @app.route("/api/video_id")
# def api_video():
#     current_video_id = get_current_video_id()
#     return jsonify({'videoId': current_video_id})
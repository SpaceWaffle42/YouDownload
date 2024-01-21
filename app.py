from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    jsonify,
    send_file
    )
from downloader import downloader as ytd
import os, time
from threading import Thread

app = Flask(__name__)

current_video_id = None

def delayed_delete_file(path, delay=10):
    def task():
        time.sleep(delay)
        try:
            os.remove(path)
            print(f"Deleted file: {path}")
        except Exception as e:
            print(f"Error deleting file: {e}")
    Thread(target=task).start()

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/process_form", methods=["POST"])
def process_form():
    global current_video_id

    try:
        link = request.form["v_link"]

        try:
            quality = request.form["res"]
        except:
            quality = "highest"

        try:
            audio_mode = request.form["a_check"]
        except:
            audio_mode = "False"

        video_return = ytd(link, quality, audio_mode)
        current_video_id = video_return

        if video_return:
            file_path = ytd(link, quality, audio_mode)[1]
            if file_path:
                response = send_file(file_path, as_attachment=True, download_name=os.path.basename(file_path))
                delayed_delete_file(file_path, delay=10)
                return response
            else:
                print("No file path returned from downloader.")
                return redirect(url_for("index"))
        else:
            print("Video ID not found or error in downloader.")
            return redirect(url_for("index"))

    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for("index"))

@app.route("/api/video_id", methods=["GET"])
def api_video():
    global current_video_id
    if current_video_id:
        return jsonify({'videoId': current_video_id[0]})
    else:
        return jsonify({'error': 'Video ID not available'}), 404

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0", port=5000)

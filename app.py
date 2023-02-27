from io import BytesIO

from flask import Flask, request, render_template, send_file
from pytube import YouTube

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/output', methods=['POST'])
def output():
    if request.method == 'POST':
        buffer = BytesIO()
        url_value = request.form.get("search-bar", None)
        resolution = request.form.get("switch-two", None)
        yt = YouTube(url_value)
        extension = ".webm" if resolution == "saq" or resolution == "caq" else ".mp4"
        file_name = yt.streams.filter().get_audio_only().default_filename
        file_name = file_name[0:file_name.rindex(".")] + extension
        mime_type = "audio/webm" if resolution == "saq" else "audio/webm" if resolution == "caq" else "video/mp4"
        audio_bitrate = "160kbps" if resolution == "saq" else "50kbps"
        if resolution == "saq" or resolution == "caq":
            audio = yt.streams.filter(abr=audio_bitrate).last()
            audio.stream_to_buffer(buffer)
            buffer.seek(0)
        else:
            i_tag = 137 if resolution == "1080p" else 22 if resolution == "720p" else 135 if resolution == "480p" else 18
            video = yt.streams.get_by_itag(i_tag)
            video.stream_to_buffer(buffer)
            buffer.seek(0)
        return send_file(buffer, download_name=file_name, as_attachment=True, mimetype=mime_type)


if __name__ == '__main__':
    app.run()

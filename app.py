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
        file_name = yt.streams.filter().get_audio_only().default_filename
        if resolution == "1080p":
            video = yt.streams.get_by_itag(137)
            video.stream_to_buffer(buffer)
            buffer.seek(0)
            extension = ".mp4"
            mime_type = "video/mp4"
        elif resolution == "720p":
            video = yt.streams.get_by_itag(22)
            video.stream_to_buffer(buffer)
            buffer.seek(0)
            extension = ".mp4"
            mime_type = "video/mp4"
        else:
            audio = yt.streams.filter(only_audio=True).first()
            audio.stream_to_buffer(buffer)
            buffer.seek(0)
            extension = ".mp3"
            mime_type = "audio/mp3"
        file_name = file_name[0:file_name.rindex(".")] + extension
        return send_file(buffer, download_name=file_name, as_attachment=True, mimetype=mime_type)


if __name__ == '__main__':
    app.run()

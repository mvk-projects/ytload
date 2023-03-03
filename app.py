from io import BytesIO
import logging

from flask import Flask, request, render_template, send_file
from pytube import YouTube

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/output', methods=['POST'])
def output():
    if request.method == 'POST':

        url_value = request.form.get("search-bar", None)
        resolution = request.form.get("switch-two", None)
        yt = YouTube(url_value)
        extension = ".mp3" if resolution == "saq" else ".mp4"
        file_name = yt.streams.filter().get_audio_only().default_filename
        file_name = file_name[0:file_name.rindex(".")] + extension
        mime_type = "audio/mpeg" if resolution == "saq" else "video/mp4"
        if resolution == "saq":
            buffer = BytesIO()
            audio = yt.streams.get_lowest_resolution()
            audio.stream_to_buffer(buffer)
            buffer.seek(0)
        else:
            if resolution == "1080p":
                try:
                    buffer = BytesIO()
                    video = yt.streams.get_by_itag(137)
                    video.stream_to_buffer(buffer)
                    buffer.seek(0)
                except:
                    buffer = BytesIO()
                    video = yt.streams.get_by_itag(22)
                    video.stream_to_buffer(buffer)
                    buffer.seek(0)
            else:
                buffer = BytesIO()
                video = yt.streams.get_lowest_resolution()
                video.stream_to_buffer(buffer)
                buffer.seek(0)

        return send_file(buffer, download_name=file_name, as_attachment=True, mimetype=mime_type)


if __name__ == '__main__':
    app.run()

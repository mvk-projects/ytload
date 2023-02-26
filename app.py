import os

from flask import Flask, request, render_template, send_file
from pytube import YouTube

app = Flask(__name__)

LOCATION = "/Users/mvk/PycharmProjects/yt_downloader"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/output', methods=['POST'])
def output():
    if request.method == 'POST':
        urlvalue = request.form.get("search-bar", None)
        resolution = request.form.get("switch-two", None)
        yt = YouTube(urlvalue)
        if resolution == "1080p" or resolution == "720p":
            extension = "mp4"
            video = yt.streams.filter(res=resolution).first()
            out_file = video.download(LOCATION)
        else:
            extension = "mp3"
            audio = yt.streams.filter(only_audio=True).first()
            out_file = audio.download(LOCATION)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
        out_file = out_file[:-3]
        out_file = out_file[20:]
        out_file = out_file[out_file.rindex("/") + 1:]
        print(out_file)
        print(LOCATION)
        print(extension)
        OUTPUT_LOCATION = LOCATION + "/" + out_file + extension
        print(OUTPUT_LOCATION)
        redirect = send_file(OUTPUT_LOCATION, as_attachment=True)
        if os.path.exists(OUTPUT_LOCATION):
            os.remove(OUTPUT_LOCATION)
        return redirect


if __name__ == '__main__':
    app.run()

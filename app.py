from flask import Flask, render_template, request, redirect, send_file
from pytube import YouTube
import os
import re

app = Flask(__name__)

# Function to clean and sanitize a filename
def clean_filename(filename):
    # Remove invalid characters by using a regular expression
    return re.sub(r'[\/:*?"<>|]', '', filename)

@app.route("/", methods=["GET", "POST"])
def index():
    video_info = None
    download_link = None

    if request.method == "POST":
        youtube_url = request.form["youtube_url"]
        try:
            yt = YouTube(youtube_url)
            video_info = {
                "title": yt.title,
                "author": yt.author,
                "length": yt.length,
                "views": yt.views,
            }
            stream = yt.streams.get_highest_resolution()
            filename = clean_filename(yt.title) + ".mp4"  # Clean the filename
            stream.download(filename=os.path.join("downloads", filename))
            download_link = "/download/" + filename
        except Exception as e:
            return "Error: " + str(e)

    return render_template("index.html", video_info=video_info, download_link=download_link)

@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join("downloads", filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

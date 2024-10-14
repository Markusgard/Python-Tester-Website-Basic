"""
Assignment #7: AJAX
"""

from flask import Flask, request
import json
import datetime

app = Flask(__name__)


@app.route("/albums")
def albums():
    """Returns a list of albums (with album_id, author, and title) in JSON."""
    # TODO complete the list of albums from albums.json
    with open("./assignment-7/7_vue/data/albums.json", "r") as data:
        albumList = json.loads(data.read())
        return albumList
    
@app.route("/songs")
def songs():
    with open("./temp/assignment-7/7_vue/data/tracks.json", "r") as data:
        songList = json.loads(data.read())
        songDict = {}

        for song in songList:
            #prepares duration in integer form.
            time = str(song["length"]).strip().split(":")
            time[0] = int(time[0])
            time[1] = int(time[1])
            seconds = time[0]*60 + time[1]
            print(seconds)
            try:
                songDict.get(song["album_id"], []).append((song["title"], song["length"], seconds))
            except:
                songDict[song["album_id"]] = [(song["title"], song["length"], seconds)]
        return songDict


@app.route("/albuminfo")
def albuminfo():
    album_id = request.args.get("album_id", None)
    if album_id:
        # TODO complete: return info on one album, including tracks
        with open("./assignment-7/7_vue/data/albums.json", "r") as data:
            albumList = json.loads(data.read())
            for album in albumList:
                if album["album_id"] == album_id:
                    return album
    return ""


@app.route("/sample")
def sample():
    return app.send_static_file("index_static.html")


@app.route("/")
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(debug=True)

from crypt import methods
from flask import Flask, render_template, request, redirect, make_response
from flaskr.player import Player
from flaskr.scoreboard import Scoreboard
from flaskr.json_encoder import JSONEncoder
import os
import threading
import requests
import time

app = Flask(__name__)

players = {}
# scoreboard = Scoreboard(os.getenv('LENIENT'))
scoreboard = {}
player_threads = {}
encoder = JSONEncoder()
lock = threading.Lock()

QUESTION_TIMEOUT = 10
QUESTION_DELAY = 5


@app.route("/")
def index():
    return render_template("leaderboard.html", leaderboard=scoreboard)


@app.route("/players", methods=["GET", "POST"])
def add_player():
    if request.method == "GET":
        return encoder.encode(players)
        #return render_temp, late("add_player.html")
    else:
        player = Player(request.form["name"], request.form["url"])
        # scoreboard.new_player(player)
        scoreboard[player] = 0
        players[player.uuid] = player
        player_thread = threading.Thread(target=sendQuestion, args=(player,))
        player_threads[player.uuid] = player_thread
        player_thread.start()
        r = make_response(render_template("player_added.html", player_id=player.uuid))
        r.headers.set("UUID", player.uuid)
        return r


@app.get("/players/<id>")
def player_page(id):
    player = players[id]
    return render_template("personal_page.html", name=player.name, id=player.uuid)


@app.get("/withdraw/<id>")
def remove_player(id):
    assert id in player_threads

    players[id].active = False
    del player_threads[id]
    del scoreboard[players[id]]

    lock.acquire()
    del players[id]
    lock.release()
    
    return redirect("/")


def sendQuestion(player):
    while player.active:
        r = None
        try:
            r = requests.get(
                player.url, params={"q": "What is your name?"}, timeout=QUESTION_TIMEOUT
            ).text
        except Exception:
            print("Connection Timeout")

        lock.acquire()
        if player in scoreboard: 
            if r == None:
                scoreboard[player] -= 50
            elif r == player.name:
                scoreboard[player] += 100
            else:
                scoreboard[player] -= 20
        lock.release()
        time.sleep(QUESTION_DELAY)

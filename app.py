from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

users = {}  # Stores username and scores
clicks_enabled = True
host_password = "securepassword"


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("check_username")
def check_username(data):
    username = data.get("username")
    password = data.get("password")
    if username == "host" and password != host_password:
        emit("login_error", {"error": "Invalid host password"})
    else:
        if username not in users:
            users[username] = 0
        users[username] = users.get(username, 0)
        emit(
            "login_success",
            {"leaderboard": get_leaderboard(), "clicks_enabled": clicks_enabled},
        )
        emit("update_player_list", {"players": list(users.keys())}, broadcast=True)


@socketio.on("increment_counter")
def increment_counter(data):
    global clicks_enabled
    if not clicks_enabled:
        return
    username = data.get("username")
    if username in users:
        users[username] += 1
    else:
        users[username] = 1

    emit("update_leaderboard", {"leaderboard": get_leaderboard()}, broadcast=True)


@socketio.on("reset_game")
def reset_game(data):
    username = data.get("username")
    password = data.get("password")
    if username == "host" and password == host_password:
        users.clear()
        emit("update_leaderboard", {"leaderboard": get_leaderboard()}, broadcast=True)


@socketio.on("toggle_clicks")
def toggle_clicks(data):
    global clicks_enabled
    username = data.get("username")
    password = data.get("password")
    if username == "host" and password == host_password:
        clicks_enabled = not clicks_enabled
        emit("clicks_toggled", {"clicks_enabled": clicks_enabled}, broadcast=True)

def get_leaderboard():
    return sorted(users.items(), key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)
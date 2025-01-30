from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.secret_key = "your_secret_key"  # To secure cookies, optional but recommended
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("welcome.html")

@app.route("/chat")
def chat():
    return render_template("index.html")

@socketio.on("message")
def handle_message(msg):
    # Assuming user data is passed with the message
    username = msg.get("username", "Guest")
    message = msg.get("message", "")
    print(f"Message received: {message} from {username}")
    
    # Send the message back to all clients
    socketio.emit("message", {"username": username, "message": message},include_self=False
                  )

if __name__ == "__main__":
    socketio.run(app,host='0.0.0.0', debug=True)

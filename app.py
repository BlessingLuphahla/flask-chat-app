from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import os
import base64
from werkzeug.utils import secure_filename
from threading import Thread
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"  # To secure cookies, optional but recommended
socketio = SocketIO(app, cors_allowed_origins="*", engineio_logger=True, logger=True)

app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

@app.route("/")
def index():
    return render_template("welcome.html")

@app.route("/chat")
def chat():
    return render_template("index.html")

@app.route("/uploads/")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

def save_file(file_data, file_path):
    try:
        if "," in file_data:
            base64_data = file_data.split(",")[1]
        else:
            return

        with open(file_path, "wb") as f:
            f.write(base64.b64decode(base64_data))
    except Exception as e:
        print(f"Error saving file: {e}")

@socketio.on("message")
def handle_message(msg):
    username = msg.get("username", "Guest")
    message = msg.get("message", "")
    
    # Send the message back to all clients
    emit("message", {"username": username, "message": message}, include_self=False)

@socketio.on("file")
def handle_file(file_data):
    try:
        filename = secure_filename(file_data["filename"])
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # Save file in background thread to prevent blocking
        thread = Thread(target=save_file, args=(file_data["file"], file_path))
        thread.start()

        # Emit file event to all users except sender
        emit("file", { "username": file_data["username"],
            "filename": filename,
            "filetype": file_data["filetype"],
            "url": f"/uploads/{filename}"  # Send a URL for the file
        }, include_self=False)

    except Exception as e:
        error_message = f"Error handling file: {str(e)}"
        emit('error', error_message)

if __name__ == "_main_":
    socketio.run(app, host="0.0.0.0", debug=True)
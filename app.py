from flask import Flask, render_template, request, jsonify,send_from_directory
from flask_socketio import SocketIO, send
import os
import base64
from werkzeug.utils import secure_filename

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

# Serve uploaded files
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@socketio.on("message")
def handle_message(msg):
    # Assuming user data is passed with the message
    username = msg.get("username", "Guest")
    message = msg.get("message", "")
    
    print(message)
    
    # Send the message back to all clients
    socketio.emit("message", {"username": username, "message": message},include_self=False
                  )
    
@socketio.on("file")
def handle_file(file_data):
    try:
        filename = secure_filename(file_data["filename"])
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # Extract base64 part
        if "," in file_data["file"]:
            base64_data = file_data["file"].split(",")[1]
        else:
            return

        # Decode and save file
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(base64_data))

        # Emit file event to all users except sender
        socketio.emit("file", {
            "username": file_data["username"],
            "filename": filename,
            "filetype": file_data["filetype"],
            "url": f"/uploads/{filename}"  # Send a URL for the file
        }, include_self=False)  # Make sure sender is excluded

    except Exception as e:
        error_message = f"Error handling file: {str(e)}"
        socketio.emit('error', error_message)



if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0")

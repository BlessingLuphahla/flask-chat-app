# Real-Time Messaging App

A real-time messaging app built with Flask, Socket.IO, and JavaScript.

## Features

* Real-time messaging
* User authentication
* Chat log display
* Disconnection handling

## How it Works

The app uses Flask as the backend framework and Socket.IO for real-time communication. When a user sends a message, it is broadcast to all connected clients, who then update their chat logs accordingly.

## Requirements

* Python 3.x
* Flask
* Socket.IO
* JavaScript

## Installation

1. Clone the repository: `git clone https://github.com/BlessingLuphahla/flask-chat-app.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`

## Usage

1. Open two or more browser windows and navigate to `http://localhost:5000`
2. Send messages by typing in the input field and pressing enter
3. View the chat log by scrolling up

## Troubleshooting

* Connection problems: Check that the server is running and that you have a stable internet connection
* Message sending issues: Check that you have entered a valid message and that the server is receiving the message

## Contributing

* Submit bug reports: [https://github.com/BlessingLuphahla/flask-chat-app/issues](https://github.com/BlessingLuphahla/flask-chat-app/issues)
* Submit feature requests: [https://github.com/BlessingLuphahla/flask-chat-app/issues](https://github.com/BlessingLuphahla/flask-chat-app/issues)
* Contribute code changes: [https://github.com/BlessingLuphahla/flask-chat-app/pulls](https://github.com/BlessingLuphahla/flask-chat-app/pulls)

## License

This project is released under the MIT license.

## Acknowledgments

* Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
* Socket.IO: [https://socket.io/](https://socket.io/)
* JavaScript: [https://www.javascript.com/](https://www.javascript.com/)
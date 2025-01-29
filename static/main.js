// Retrieve user info from sessionStorage
var username = sessionStorage.getItem("username") || "Guest";
var userID = sessionStorage.getItem("userID") || "0000";

// Display username in chat header
document.getElementById("chat-header").innerText = `Welcome, ${username}`;

// Connect to the Flask server using SocketIO
var socket = io.connect("http://" + document.domain + ":" + location.port);

// Listen for incoming messages
socket.on("message", function (data) {
  addMessage(data.username, data.message, data.username === username ? "user" : "other");
});

// Add messages to chat box with different classes for user and other participants
function addMessage(sender, msg, senderType) {
  var chatBox = document.getElementById("chat-box");
  var messageElement = document.createElement("div");

  // Assign class based on senderType
  messageElement.classList.add("message", senderType === "user" ? "user-message" : "sender-message");

  // Format message with the sender's name
  var messageContent = `<strong>${sender}</strong>: ${msg}`;
  messageElement.innerHTML = messageContent;

  chatBox.appendChild(messageElement);
  chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to latest message
}

// Send message to Flask server
function sendMessage() {
  var inputField = document.getElementById("message");
  var message = inputField.value.trim();

  if (message !== "") {
    // Emit message with user info
    socket.emit("message", {
      username: username,
      message: message,
    });

    // Display sent message in chat box with 'user' class
    addMessage(username, message, "user");

    inputField.value = ""; // Clear input field after sending
  }
}

// Allow sending message by pressing "Enter"
function handleKeyPress(event) {
  if (event.key === "Enter" && !event.shiftKey) {
    sendMessage();
  }
}

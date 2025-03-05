// Retrieve user info from sessionStorage
var username = sessionStorage.getItem("username") || "Guest";
var userID = sessionStorage.getItem("userID") || "0000";
const chatBox = document.getElementById("chat-box");

// Display username in chat header
document.getElementById("chat-header").innerText = `Welcome, ${username}`;

// event listeners

// Connect to the Flask server using SocketIO

var socket = io.connect(
  window.location.protocol + "//" + window.location.host,
  {
    transports: ["websocket"],
  }
);

// Listen for incoming messages
socket.on("message", function (data) {
  addMessage(
    data.username,
    data.message,
    data.username === username ? "user" : "other"
  );
});

// Add messages to chat box with different classes for user and other participants
function addMessage(sender, msg, senderType) {
  var messageElement = document.createElement("div");

  // Assign class based on senderType

  messageElement.classList.add(
    "message",
    senderType === "user" ? "user-message" : "sender-message"
  );

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

  message = message.replace("/\n/g", "<br>");

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

// Allow sending message by pressing "Space"
function handleKeyPress(event) {
  // var inputField = document.getElementById("message");
  // if (event.key === "Enter" && !event.shiftKey) {
  //   inputField.value = inputField.value + "<br/>";
  //   console.log(inputField.value);
  // }
}

function sendFile(file) {
  var reader = new FileReader();
  reader.onload = function (event) {
    var fileData = event.target.result; // Data URL

    // Send base64 file to Flask server
    socket.emit("file", {
      username: username,
      file: fileData,
      filename: file.name,
      filetype: file.type,
    });
  };
  reader.readAsDataURL(file);
}

function handleFileSelection(event) {
  var file = event.target.files[0];
  if (file) {
    sendFile(file);
  }
}

document
  .getElementById("file-input")
  .addEventListener("change", handleFileSelection);

// Listen for file events from the server
socket.on("file", function (data) {
  sendAFile(data.username, data, data.username === username ? "user" : "other");
});

function sendAFile(sender, data, senderType) {
  var messageElement = document.createElement("div");
  messageElement.classList.add(
    "message",
    senderType === "user" ? "user-message" : "sender-message"
  );

  // Display file with a download link
  var messageContent = `<strong>${data.username}</strong>: <a class="uploadLink" href="/uploads/${data.filename}" target="_blank">${data.filename}</a>`;
  messageElement.innerHTML = messageContent;

  chatBox.appendChild(messageElement);
  chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll
}

socket.on("error", (errorMessage) => {
  console.error(errorMessage);
  // Display the error message to the user
  alert(errorMessage);
});
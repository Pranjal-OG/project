// chat.js

document.addEventListener("DOMContentLoaded", () => {
    const socket = io();
    const form = document.getElementById("chat-form");
    const input = document.getElementById("message");
    const messagesDiv = document.getElementById("messages");
    const username = document.getElementById("username").value;

    socket.on("connect", () => {
        console.log("Connected to server");
    });

    socket.on("receive_message", (data) => {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message");

        if (data.sender === username) {
            msgDiv.classList.add("PRANJAL");
        } else {
            msgDiv.classList.add("MADHURIMA");
        }

        msgDiv.textContent = `${data.sender}: ${data.message}`;
        messagesDiv.appendChild(msgDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const message = input.value.trim();
        if (message.length === 0) return;

        socket.emit("send_message", {
            message: message,
            sender: username
        });

        input.value = "";
    });
});

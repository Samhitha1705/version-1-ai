const chatToggle = document.getElementById("chat-toggle");
const chatContainer = document.getElementById("chat-container");
const closeChat = document.getElementById("close-chat");
const chatBody = document.getElementById("chat-body");
const inputField = document.getElementById("user-input");

chatToggle.addEventListener("click", () => {
    chatContainer.style.display = "flex";
    setTimeout(() => inputField.focus(), 100);
});

closeChat.addEventListener("click", () => {
    chatContainer.style.display = "none";
});

function addBotMessage(msg, isHTML = false) {
    const formatted = isHTML ? msg : msg.replace(/\n/g, "<br>");
    chatBody.innerHTML += `<div class="bot-message">${formatted}</div>`;
    chatBody.scrollTop = chatBody.scrollHeight;
    inputField.focus();
}

function addUserMessage(msg) {
    chatBody.innerHTML += `<div class="user-message">${msg}</div>`;
    chatBody.scrollTop = chatBody.scrollHeight;
}

// Send message
function sendMessage() {
    const msg = inputField.value.trim();
    if (!msg) return;
    addUserMessage(msg);
    inputField.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => addBotMessage(data.reply));
}

// Quick buttons
function sendQuick(msg) {
    addUserMessage(msg);

    if (msg.toLowerCase() === "booking") {
        const dateHTML = `
            📅 Please select a <strong>date (YYYY-MM-DD)</strong>:
            <input type="date" id="booking-date"/>
            <input type="time" id="booking-time"/>
            <button onclick="confirmBooking()">Confirm</button>
        `;
        addBotMessage(dateHTML, true);
        return;
    }

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => addBotMessage(data.reply));
}

// Confirm booking
function confirmBooking() {
    const date = document.getElementById("booking-date").value;
    const time = document.getElementById("booking-time").value;

    if (!date || !time) {
        alert("Please select both date and time!");
        return;
    }

    addBotMessage(`
        ✅ Your consultation is booked on <strong>${date}</strong> at <strong>${time} IST</strong>.<br>
        For support: support@nutrisense.com
    `, true);
}

// ENTER key support
inputField.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

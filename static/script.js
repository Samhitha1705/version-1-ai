const toggleBtn = document.getElementById("chat-toggle");
const chatContainer = document.getElementById("chat-container");
const closeBtn = document.getElementById("close-chat");
const input = document.getElementById("user-input");
const chatBody = document.getElementById("chat-body");

/* OPEN CHAT */
toggleBtn.onclick = () => {
    chatContainer.style.display = "flex";
    document.body.style.overflow = "hidden"; // prevent page scroll
    input.focus();
};

/* CLOSE CHAT */
closeBtn.onclick = () => {
    chatContainer.style.display = "none";
    document.body.style.overflow = "auto";
};

/* APPEND USER MESSAGE */
function appendUser(msg) {
    chatBody.innerHTML += `<div class="user-message">${msg}</div>`;
    chatBody.scrollTop = chatBody.scrollHeight;
}

/* APPEND BOT MESSAGE */
function appendBot(msg) {
    chatBody.innerHTML += `<div class="bot-message">${msg.replace(/\n/g, "<br>")}</div>`;
    chatBody.scrollTop = chatBody.scrollHeight;
}

/* SEND MESSAGE */
window.sendMessage = function () {
    const msg = input.value.trim();
    if (!msg) return;

    appendUser(msg);
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => handleBotResponse(data.reply));
};

/* QUICK BUTTON */
window.sendQuick = function (text) {
    appendUser(text);

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
    })
    .then(res => res.json())
    .then(data => handleBotResponse(data.reply));
};

/* HANDLE BOT RESPONSE */
function handleBotResponse(msg) {

    if (msg.includes("Please select a **date**")) {
        appendBot(msg);
        chatBody.innerHTML += `
            <div class="user-message">
                <input type="date" id="booking-date">
                <button onclick="sendDate()">Submit</button>
            </div>`;
    }
    else if (msg.includes("Enter a **time")) {
        appendBot(msg);
        chatBody.innerHTML += `
            <div class="user-message">
                <input type="time" id="booking-time">
                <button onclick="sendTime()">Submit</button>
            </div>`;
    }
    else {
        appendBot(msg);
    }

    chatBody.scrollTop = chatBody.scrollHeight;
}

/* DATE */
window.sendDate = function () {
    const date = document.getElementById("booking-date").value;
    if (!date) return alert("Select date");
    sendQuick(date);
};

/* TIME */
window.sendTime = function () {
    const time = document.getElementById("booking-time").value;
    if (!time) return alert("Select time");
    sendQuick(time);
};

/* ENTER KEY */
input.addEventListener("keydown", e => {
    if (e.key === "Enter") sendMessage();
});

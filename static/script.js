const toggleBtn = document.getElementById("chat-toggle");
const chatContainer = document.getElementById("chat-container");
const closeBtn = document.getElementById("close-chat");
const input = document.getElementById("user-input");
const chatBody = document.getElementById("chat-body");
 
toggleBtn.onclick = () => { chatContainer.style.display = "flex"; input.focus(); };
closeBtn.onclick = () => { chatContainer.style.display = "none"; };
 
function appendUser(msg) {
    chatBody.innerHTML += `<div class="user-message">${msg}</div>`;
    chatBody.scrollTop = chatBody.scrollHeight;
}
 
function appendBot(msg) {
    chatBody.innerHTML += `<div class="bot-message">${msg.replace(/\n/g, "<br>")}</div>`;
    chatBody.scrollTop = chatBody.scrollHeight;
}
 
function sendMessage() {
    const msg = input.value.trim();
    if (!msg) return;
    appendUser(msg);
    input.value = "";
 
    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: msg})
    })
    .then(res => res.json())
    .then(data => handleBotResponse(data.reply));
}
 
function sendQuick(text) {
    appendUser(text);
    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: text})
    })
    .then(res => res.json())
    .then(data => handleBotResponse(data.reply));
}
 
function handleBotResponse(msg) {
    if (msg.includes("Please select a **date**")) {
        chatBody.innerHTML += `<div class="bot-message">${msg.replace(/\n/g,"<br>")}</div>`;
        chatBody.innerHTML += `
            <div class="user-message">
                <input type="date" id="booking-date" />
                <button onclick="sendDate()">Submit Date</button>
            </div>
        `;
    } else if (msg.includes("Enter a **time")) {
        chatBody.innerHTML += `<div class="bot-message">${msg.replace(/\n/g,"<br>")}</div>`;
        chatBody.innerHTML += `
            <div class="user-message">
                <input type="time" id="booking-time" />
                <button onclick="sendTime()">Submit Time</button>
            </div>
        `;
    } else {
        appendBot(msg);
    }
    chatBody.scrollTop = chatBody.scrollHeight;
}
 
function sendDate() {
    const dateInput = document.getElementById("booking-date");
    if (!dateInput.value) return alert("Please select a date.");
    sendQuick(dateInput.value);
}
 
function sendTime() {
    const timeInput = document.getElementById("booking-time");
    if (!timeInput.value) return alert("Please select time.");
    sendQuick(timeInput.value);
}
 
// Enter key support
input.addEventListener("keydown", e => {
    if (e.key === "Enter") { e.preventDefault(); sendMessage(); }
});
 
 
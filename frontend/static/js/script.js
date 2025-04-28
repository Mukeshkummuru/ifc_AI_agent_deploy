const examples = [
    "How many walls?",
    "Give total wall volume",
    "What is the slab volume?",
    "Show surface area of walls"
];

let current = 0;
setInterval(() => {
    document.getElementById("user-input").placeholder = examples[current];
    current = (current + 1) % examples.length;
}, 5000);

function sendQuery() {
    const input = document.getElementById("user-input");
    const spinner = document.getElementById("loading-spinner");
    const chatBox = document.getElementById("chat-box");
    const message = input.value.trim();
    if (!message) return;

    chatBox.innerHTML += `<p><strong>You:</strong> ${message}</p>`;
    input.value = "";
    spinner.style.display = "inline-block"; // Show spinner

    // Send to backend
    fetch("http://127.0.0.1:5000/query", {   // 👈 USE FULL URL LOCALLY
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => {
        chatBox.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(err => {
        chatBox.innerHTML += `<p><strong>Bot:</strong> Error occurred.</p>`;
    })
    .finally(() => {
        spinner.style.display = "none"; // Hide spinner after response
    });
}

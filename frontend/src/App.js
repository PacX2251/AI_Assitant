// app.js
const backendUrl = "http://localhost:8000"; // Cambia a tu URL de producción

// Subir archivo al backend
async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${backendUrl}/upload`, {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    alert(`File uploaded: ${data.filename}`);
}

// Enviar mensaje de chat al backend
async function sendMessage() {
    const messageInput = document.getElementById("messageInput");
    const message = messageInput.value;

    if (!message) {
        alert("Please enter a message.");
        return;
    }

    const response = await fetch(`${backendUrl}/chat`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: message })
    });

    const data = await response.json();

    // Mostrar la respuesta en el chat
    const chatBox = document.getElementById("chatBox");
    chatBox.innerHTML += `<div class="user-msg"><b>You:</b> ${message}</div>`;
    chatBox.innerHTML += `<div class="bot-msg"><b>Bot:</b> ${data.answer}</div>`;

    messageInput.value = "";
}

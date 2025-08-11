import React, { useState } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    { id: 1, from: "bot", text: "👋 Hi! Upload one or more files or type a message to start." },
  ]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { id: messages.length + 1, from: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();
      const botMessage = { id: messages.length + 2, from: "bot", text: data.reply };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        { id: messages.length + 2, from: "bot", text: "❌ Server connection failed." },
      ]);
    }

    setInput("");
  };

  const handleFileUpload = async (e) => {
    const files = e.target.files;
    if (!files.length) return;

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      setMessages((prev) => [
        ...prev,
        { id: prev.length + 1, from: "bot", text: `✅ Files processed: ${result.message}` },
      ]);
    } catch (error) {
      console.error("File upload error:", error);
      setMessages((prev) => [
        ...prev,
        { id: prev.length + 1, from: "bot", text: "❌ File upload failed." },
      ]);
    }

    e.target.value = null;
  };

  return (
    <div className="app-container">
      {/* Sidebar siempre visible */}
      <div className="sidebar">
        <h2>📤 Upload Files</h2>
        <input type="file" onChange={handleFileUpload} multiple />
      </div>

      {/* Chat principal */}
      <main className="chat-container">
        <div className="messages">
          {messages.map((msg) => (
            <div key={msg.id} className={`message ${msg.from}`}>
              {msg.text}
            </div>
          ))}
        </div>

        <div className="input-area">
         <textarea
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
                }
            }}
            rows={3}
            />
          <button onClick={handleSend}>Send</button>
        </div>
      </main>
    </div>
  );
}

export default App;

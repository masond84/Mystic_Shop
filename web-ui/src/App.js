import React, { useState, useRef, useEffect } from "react";
import './App.css';

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [history, setHistory] = useState([]);
  const [input, setInput] = useState("");
  const outputRef = useRef(null);

  useEffect(() => {
    fetch(`${API_URL}/history`)
      .then(res => res.json())
      .then(data => setHistory(data.output.split("\n")))
      .catch(err => console.error("Failed to fetch history:", err));
  }, []);
 
  const sendCommand = async () => {
    if (!input.trim()) return;

    try {
      const res = await fetch("http://127.0.0.1:8000/command", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input })
      });
      const data = await res.json();
      setHistory(data.output.split("\n"));
    } catch (err) {
      setHistory(prev => [...prev, `❌ Network error: ${err.message}`]);
    }

    setInput("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendCommand();
  };

  // Auto scroll to bottom
  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [history]);

  return (
    <div style={{ backgroundColor: "#1e1e1e", color: "#e5e5e5", height: "100vh", padding: "20px", fontFamily: "monospace" }}>
      <h1>Mystic Shop - Web Console</h1>
      <div
        ref={outputRef}
        style={{
          backgroundColor: "#2e2e2e",
          padding: "10px",
          height: "70vh",
          overflowY: "auto",
          whiteSpace: "pre-wrap",
          border: "1px solid #555",
          marginBottom: "10px"
        }}
      >
        {history.map((line, index) => <div key={index}>{line}</div>)}
      </div>
      <input
        style={{ width: "100%", padding: "10px", backgroundColor: "#1e1e1e", color: "#e5e5e5", border: "1px solid #555" }}
        placeholder="Type your command and press Enter"
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyPress={handleKeyPress}
      />
    </div>
  );
}

export default App;
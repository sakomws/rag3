import { useState } from "react";
import styles from "./Chatbot.module.css";

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async (event) => {
    event.preventDefault();
    if (input !== "") {
      setMessages([...messages, { text: input, user: "User" }]);

      // send user prompt to gpt to classify whether or not it is real time or not real time
      const response = await fetch("http://localhost:8000/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: input,
        }),
      });

      const data = await response.json();

      setInput("");
    }
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.textBox}>
        {messages.map((message, index) => (
          <p key={index}>
            <strong>{message.user}</strong> {message.text}
          </p>
        ))}
      </div>
      <form onSubmit={sendMessage}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          type="text"
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default Chatbot;

import { useState } from "react";
import styles from "./Chatbot.module.css";

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = (event) => {
    event.preventDefault();
    if (input !== "") {
      setMessages([...messages, { text: input, user: "User" }]);
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

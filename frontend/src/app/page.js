"use client";

import Chatbot from "../components/chatbot";
import styles from "./Home.module.css";

export default function Home() {
  return (
    <div className={styles.container}>
      <Chatbot />
    </div>
  );
}

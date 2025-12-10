import React, { useState } from "react";

const API_URL = "https://spam-detection-backend-vbzq.onrender.com";

const SpamChecker = () => {
  const [input, setInput] = useState("");
  const [result, setResult] = useState("");
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleCheck = async () => {
    setLoading(true);
    setResult("");
    setConfidence(null);
    setError("");

    try {
      const response = await fetch(`${API_URL}/check_spam`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: input }),
      });

      if (!response.ok) {
        throw new Error("Backend error");
      }

      const data = await response.json();
      setResult(data.label);
      setConfidence(data.confidence);
    } catch (err) {
      console.error(err);
      setError("Error connecting to backend");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1 className="title">SPAM DETECTOR</h1>

      <textarea
        placeholder="Paste your email or SMS here..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      ></textarea>

      <button onClick={handleCheck} disabled={loading}>
        CHECK
      </button>

      {loading && <div className="loader"><div className="ring"></div></div>}

      {!loading && result === "safe" && (
        <div className="result safe">
          ✔ SAFE
          <div className="confidence">
            Confidence: {(confidence * 100).toFixed(1)}%
          </div>
        </div>
      )}

      {!loading && result === "spam" && (
        <div className="result spam">
          ⚠ SPAM DETECTED
          <div className="confidence">
            Confidence: {(confidence * 100).toFixed(1)}%
          </div>
        </div>
      )}

      {!loading && error && (
        <div className="result spam">❌ {error}</div>
      )}
    </div>
  );
};

export default SpamChecker;

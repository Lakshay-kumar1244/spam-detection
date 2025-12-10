import React, { useState } from "react";

const SpamChecker = () => {
  const [input, setInput] = useState("");
  const [result, setResult] = useState("");
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCheck = async () => {
    setLoading(true);
    setResult("");
    setConfidence(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/check_spam", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input }),
      });

      const data = await response.json();

      // ✅ FIXED FOR NEW BACKEND RESPONSE
      setResult(data.label);          // "spam" or "safe"
      setConfidence(data.confidence); // number
    } catch {
      setResult("error");
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

      <button onClick={handleCheck}>CHECK</button>

      {loading && (
        <div className="loader">
          <div className="ring"></div>
        </div>
      )}

      {!loading && result === "safe" && (
        <div className="result safe">
          ✔ SAFE
          {confidence !== null && (
            <div className="confidence">
              Confidence: {(confidence * 100).toFixed(1)}%
            </div>
          )}
        </div>
      )}

      {!loading && result === "spam" && (
        <div className="result spam">
          ⚠ SPAM DETECTED
          {confidence !== null && (
            <div className="confidence">
              Confidence: {(confidence * 100).toFixed(1)}%
            </div>
          )}
        </div>
      )}

      {!loading && result === "error" && (
        <div className="result spam">
          ❌ Error connecting to backend
        </div>
      )}
    </div>
  );
};

export default SpamChecker;

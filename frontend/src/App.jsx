import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askAgent = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");

    try {
      const response = await fetch("http://127.0.0.1:8001/agent", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Request failed");
      }

      setAnswer(data.answer);
    } catch (error) {
      setAnswer(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const quickQuestion = (text) => {
    setQuestion(text);
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Agentic Insurance Operations Assistant</h1>
          <p>
            AI-powered claims, policy, and insurance operations assistant
          </p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          AI Assistant Online
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <h2>How can I help with insurance operations?</h2>
          <p>
            Ask about claims, priorities, policies, analytics, or claim
            processing rules.
          </p>
        </section>

        <section className="chat-card">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Example: What is the status of claim 1001?"
            rows="4"
          />

          <button onClick={askAgent} disabled={loading}>
            {loading ? "Thinking..." : "Ask AI Agent"}
          </button>

          {answer && (
            <div className="answer">
              <h3>AI Agent Response</h3>
              <p>{answer}</p>
            </div>
          )}
        </section>

        <section className="quick-section">
          <h3>Try a question</h3>

          <div className="quick-grid">
            <button
              onClick={() =>
                quickQuestion("What is the status of claim 1001?")
              }
            >
              Claim 1001 Status
            </button>

            <button
              onClick={() =>
                quickQuestion("Show me all high-priority claims")
              }
            >
              High-Priority Claims
            </button>

            <button
              onClick={() =>
                quickQuestion("What happens when a claim is rejected?")
              }
            >
              Rejected Claims Policy
            </button>

            <button
              onClick={() =>
                quickQuestion("Give me claim statistics and analytics")
              }
            >
              Claim Analytics
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
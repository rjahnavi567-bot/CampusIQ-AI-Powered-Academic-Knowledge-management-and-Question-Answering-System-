import { useEffect, useState } from "react";
import { api } from "../api/api";

export default function History() {

  const [history, setHistory] = useState([]);

  const loadHistory = async () => {

    try {

      const res = await api.get("/history");

      setHistory(res.data);

    } catch (error) {

      console.error(error);

    }

  };

  useEffect(() => {

    loadHistory();

  }, []);

  const clearHistory = async () => {

    const confirmDelete =
      window.confirm(
        "Clear all question history?"
      );

    if (!confirmDelete) return;

    try {

      await api.delete("/history");

      setHistory([]);

    } catch (error) {

      console.error(error);

    }

  };

  return (

    <div className="page-card">

      <h1>📜 Question History</h1>

      <button
        onClick={clearHistory}
      >
        Clear History
      </button>

      <br />
      <br />

      {
        history.length === 0
        ? (
          <p>No history available.</p>
        )
        : (
          history.map((item) => (

            <div
              key={item.id}
              className="history-card"
            >

              <h3>
                ❓ {item.question}
              </h3>

              <p>
                <strong>
                  Asked:
                </strong>{" "}
                {
                  new Date(
                    item.created_at
                  ).toLocaleString()
                }
              </p>

              <hr />

              <pre>
                {item.answer}
              </pre>

            </div>

          ))
        )
      }

    </div>

  );
}
import { useEffect, useState } from "react";
import { api } from "../api/api";

export default function GroupedHistory() {

  const [history, setHistory] =
    useState({});

  useEffect(() => {

    loadHistory();

  }, []);

  const loadHistory = async () => {

    const res =
      await api.get(
        "/history/grouped"
      );

    setHistory(
      res.data
    );
  };

  return (
    <div
      style={{
        padding: "30px"
      }}
    >

      <h1>
        📚 Questions By Document
      </h1>

      {
        Object.keys(history)
          .sort()
          .map((doc) => (

            <div
              key={doc}
              className="page-card"
            >

              <h2>
                📄 {doc}
              </h2>

              <ul>

                {
                  history[doc]
                  .map((q) => (

                    <li
                      key={q.id}
                      style={{
                        marginBottom:
                          "10px"
                      }}
                    >
                      {q.question}
                    </li>

                  ))
                }

              </ul>

            </div>

          ))
      }

    </div>
  );
}
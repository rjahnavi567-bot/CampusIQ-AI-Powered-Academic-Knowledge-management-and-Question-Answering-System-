import { useState } from "react";
import { api } from "../api/api";

export default function SearchDocuments() {

  const [query, setQuery] = useState("");

  const [results, setResults] = useState([]);

  const search = async () => {

    if (!query.trim()) return;

    try {

      const res = await api.get(
        `/search-documents?query=${query}`
      );

      setResults(res.data);

    } catch (err) {

      console.log(err);

    }
  };
  const highlightText = (
  text,
  keyword
) => {

  if (!keyword) return text;

  const regex = new RegExp(
    `(${keyword})`,
    "gi"
  );

  const parts =
    text.split(regex);

  return parts.map(
    (part, index) =>

      regex.test(part)
        ? (
            <mark
              key={index}
            >
              {part}
            </mark>
          )
        : (
            part
          )
  );
};

  return (

    <div style={{ padding: "30px" }}>

      <h1>🔍 Search Documents</h1>

      <input
        type="text"
        value={query}
        placeholder="Search inside uploaded documents..."
        onChange={(e) =>
          setQuery(e.target.value)
        }
        style={{
          width: "400px",
          padding: "10px"
        }}
      />

      <button
        onClick={search}
        style={{
          marginLeft: "10px"
        }}
      >
        Search
      </button>

      <br />
      <br />

      {results.length === 0 && (
        <p>No results yet.</p>
      )}

      {results.map((result, index) => (

        <div
          key={index}
          className="page-card"
        >

          <h3>
            📄 {result.file}
          </h3>

          <p>
            <strong>Page:</strong> {result.page}
          </p>

          <p
            style={{
              fontWeight: "bold",
              color:
                result.score >= 70
                  ? "green"
                  : result.score >= 40
                  ? "orange"
                  : "red"
            }}
          >
            Relevance: {result.score}%
          </p>

          <p
  style={{
    lineHeight: "1.8"
  }}
>
  {
    highlightText(
      result.text,
      query
    )
  }
</p>

          <button
  onClick={() =>
    window.open(
      result.url,
      "_blank"
    )
  }
  style={{
    background: "#2563eb",
    color: "white",
    border: "none",
    padding: "10px 15px",
    borderRadius: "8px",
    cursor: "pointer"
  }}
>
  📖 Open Page {result.page}
</button>

        </div>

      ))}

    </div>
  );
}
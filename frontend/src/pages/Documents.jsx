import { useEffect, useState } from "react";
import { api } from "../api/api";

export default function Documents() {
  const [docs, setDocs] = useState([]);
  const [search, setSearch] = useState("");
  const openDocument = async (
  documentId
) => {

  const res =
  await api.get(
    `/documents/${documentId}/view`
  );

  window.open(
    res.data.url,
    "_blank"
  );
};
  const loadDocuments = async () => {
    try {
      const res = await api.get("/documents");
      setDocs(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const deleteDocument = async (id) => {
    try {
      await api.delete(`/documents/${id}`);

      setDocs(
        docs.filter(
          (doc) => doc.id !== id
        )
      );
    } catch (err) {
      alert("Delete failed");
    }
  };

  const filteredDocs = docs.filter((doc) =>
    doc.filename
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <div style={{ padding: "30px" }}>
      <h1>📚 Documents</h1>

      <input
        type="text"
        placeholder="Search documents..."
        value={search}
        onChange={(e) =>
          setSearch(e.target.value)
        }
        style={{
          padding: "10px",
          width: "300px",
          marginBottom: "20px",
          borderRadius: "8px",
          border: "1px solid #ccc",
        }}
      />

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fill,minmax(300px,1fr))",
          gap: "20px",
        }}
      >
        {filteredDocs.map((doc) => (
          <div
            key={doc.id}
            style={{
              background: "white",
              padding: "20px",
              borderRadius: "12px",
              boxShadow:
                "0 2px 10px rgba(0,0,0,0.1)",
            }}
          >
            <h3>📄 {doc.filename}</h3>

            <p>
              <strong>Status:</strong>{" "}
              {doc.status}
            </p>

            <p>
              <strong>Chunks:</strong>{" "}
              {doc.chunk_count}
            </p>

            <p>
              <strong>Uploaded:</strong>{" "}
              {new Date(
                doc.created_at
              ).toLocaleDateString()}
            </p>
            <button
  onClick={() =>
    window.open(
      `http://localhost:8000/uploads/${doc.filename}`,
      "_blank"
    )
  }
  style={{
    background: "#2563eb",
    color: "white",
    border: "none",
    padding: "10px 15px",
    borderRadius: "8px",
    cursor: "pointer",
    marginRight: "10px"
  }}
>
  View
</button>
            <button
              onClick={() =>
                deleteDocument(doc.id)
              }
              style={{
                background: "#dc3545",
                color: "white",
                border: "none",
                padding:
                  "10px 15px",
                borderRadius: "8px",
                cursor: "pointer",
              }}
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
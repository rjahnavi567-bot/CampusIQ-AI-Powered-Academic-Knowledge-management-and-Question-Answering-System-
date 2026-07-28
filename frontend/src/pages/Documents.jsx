import { useEffect, useState, useRef } from "react";
import { api } from "../api/api";

export default function Documents() {
  const [docs, setDocs] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const searchTimeout = useRef(null);
  const suggestionBox = useRef(null);
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
  useEffect(() => {

    function handleClick(event) {

        if (
            suggestionBox.current &&
            !suggestionBox.current.contains(event.target)
        ) {

            setSuggestions([]);

        }

    }

    document.addEventListener(
        "click",
        handleClick
    );

    return () => {

        document.removeEventListener(
            "click",
            handleClick
        );

    };

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

  const searchDocuments = (value) => {

    setSearch(value);
    if (value.trim() === "") {

    setSuggestions([]);

}

    if (searchTimeout.current) {

        clearTimeout(searchTimeout.current);

    }

    searchTimeout.current = setTimeout(async () => {

        if (value.trim() === "") {

            loadDocuments();
            return;

        }

        try {

            setLoading(true);

            const [searchRes, suggestionRes] = await Promise.all([

    api.get(
        `/documents/search?query=${encodeURIComponent(value)}`
    ),

    api.get(
        `/documents/suggestions?query=${encodeURIComponent(value)}`
    )

]);

setDocs(searchRes.data);

setSuggestions(suggestionRes.data);

        }

        catch (err) {

            console.log(err);

        }

        finally {

            setLoading(false);

        }

    }, 300);

};

  return (
    <div style={{ padding: "30px" }}>
      <h1>📚 Documents</h1>

      <div
    ref={suggestionBox}
    style={{
        position: "relative",
        width: "320px",
        marginBottom: "20px"
    }}
>

<input
    type="text"
    placeholder="Search documents..."
    value={search}
    onChange={(e) =>
        searchDocuments(e.target.value)
    }
    style={{
        padding: "10px",
        width: "100%",
        borderRadius: "8px",
        border: "1px solid #ccc"
    }}
/>

{
suggestions.length > 0 && (

<div
style={{
    position: "absolute",
    top: "48px",
    left: 0,
    width: "100%",
    background: "white",
    border: "1px solid #ddd",
    borderRadius: "8px",
    boxShadow: "0 2px 8px rgba(0,0,0,.1)",
    zIndex: 1000
}}
>

{
suggestions.map((item,index)=>(

<div
key={index}

style={{
    padding:"10px",
    cursor:"pointer",
    borderBottom:"1px solid #eee"
}}

onClick={()=>{
    setSearch(item);
    setSuggestions([]);
    searchDocuments(item);
}}
>

📄 {item}

</div>

))
}

</div>

)
}

{
loading &&

<p
style={{
    color:"#2563eb",
    fontWeight:"bold",
    marginTop:"55px"
}}
>

🔍 Searching documents...

</p>

}

</div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fill,minmax(300px,1fr))",
          gap: "20px",
        }}
      >
        {docs.map((doc) => (
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
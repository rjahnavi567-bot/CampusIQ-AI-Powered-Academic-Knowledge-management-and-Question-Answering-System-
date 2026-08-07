import { useEffect, useState, useRef } from "react";
import { api } from "../api/api";

export default function Documents() {
  const [docs, setDocs] = useState([]);
  const [groupedDocuments, setGroupedDocuments] = useState([]);

  const [expandedSubjects, setExpandedSubjects] = useState({});

  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);

  const searchTimeout = useRef(null);
  const suggestionBox = useRef(null);

  // ==========================
  // OPEN DOCUMENT
  // ==========================

  const openDocument = async (documentId) => {
    try {
      const res = await api.get(
        `/documents/${documentId}/view`
      );

      window.open(
        res.data.url,
        "_blank"
      );
    } catch (err) {
      console.log(err);
      alert("Unable to open document");
    }
  };

  // ==========================
  // LOAD ALL DOCUMENTS
  // ==========================

  const loadDocuments = async () => {
    try {
      const res = await api.get("/documents");

      setDocs(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  // ==========================
  // LOAD GROUPED DOCUMENTS
  // ==========================

  const loadGroupedDocuments = async () => {
  try {
    const res = await api.get(
      "/documents/grouped"
    );

    setGroupedDocuments(
      res.data
    );

  } catch (err) {
    console.log(err);
  }
};

  // ==========================
  // INITIAL LOAD
  // ==========================

  useEffect(() => {
    loadDocuments();
    loadGroupedDocuments();
  }, []);

  // ==========================
  // CLOSE SEARCH SUGGESTIONS
  // ==========================

  useEffect(() => {
    function handleClick(event) {
      if (
        suggestionBox.current &&
        !suggestionBox.current.contains(
          event.target
        )
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

  // ==========================
  // TOGGLE SUBJECT
  // ==========================

  const toggleSubject = (subject) => {
    setExpandedSubjects((prev) => ({
      ...prev,
      [subject]: !prev[subject]
    }));
  };

  // ==========================
  // DELETE DOCUMENT
  // ==========================

  const deleteDocument = async (id) => {
    try {
      await api.delete(
        `/documents/${id}`
      );

      /*
       * Update normal document list
       */

      setDocs((prevDocs) =>
        prevDocs.filter(
          (doc) => doc.id !== id
        )
      );

      /*
       * Update grouped document list
       */

      setGroupedDocuments((prevGroups) =>
        prevGroups
          .map((group) => ({
            ...group,
            documents:
              group.documents.filter(
                (doc) => doc.id !== id
              )
          }))
          .filter(
            (group) =>
              group.documents.length > 0
          )
      );

    } catch (err) {
      console.log(err);
      alert("Delete failed");
    }
  };

  // ==========================
  // SEARCH DOCUMENTS
  // ==========================

  const searchDocuments = (value) => {
    setSearch(value);

    if (value.trim() === "") {
      setSuggestions([]);

      /*
       * Restore grouped view
       */

      loadGroupedDocuments();

      return;
    }

    if (searchTimeout.current) {
      clearTimeout(
        searchTimeout.current
      );
    }

    searchTimeout.current =
      setTimeout(async () => {

        if (value.trim() === "") {
          loadDocuments();
          loadGroupedDocuments();
          return;
        }

        try {
          setLoading(true);

          const [
            searchRes,
            suggestionRes
          ] = await Promise.all([

            api.get(
              `/documents/search?query=${encodeURIComponent(
                value
              )}`
            ),

            api.get(
              `/documents/suggestions?query=${encodeURIComponent(
                value
              )}`
            )

          ]);

          /*
           * Search results are shown
           * as normal cards.
           */

          setDocs(
            searchRes.data
          );

          setSuggestions(
            suggestionRes.data
          );

        } catch (err) {
          console.log(err);

        } finally {
          setLoading(false);
        }

      }, 300);
  };

  // ==========================
  // RENDER
  // ==========================

  return (
    <div
      style={{
        padding: "30px"
      }}
    >

      {/* ==========================
          PAGE TITLE
      ========================== */}

      <h1
        style={{
          marginBottom: "20px"
        }}
      >
        📚 Documents
      </h1>


      {/* ==========================
          SEARCH
      ========================== */}

      <div
        ref={suggestionBox}
        style={{
          position: "relative",
          width: "320px",
          maxWidth: "100%",
          marginBottom: "25px"
        }}
      >

        <input
          type="text"
          placeholder="Search documents..."
          value={search}
          onChange={(e) =>
            searchDocuments(
              e.target.value
            )
          }
          style={{
            padding: "10px 12px",
            width: "100%",
            boxSizing: "border-box",
            borderRadius: "8px",
            border: "1px solid #ccc",
            outline: "none"
          }}
        />


        {/* ==========================
            SEARCH SUGGESTIONS
        ========================== */}

        {suggestions.length > 0 && (

          <div
            style={{
              position: "absolute",
              top: "48px",
              left: 0,
              width: "100%",
              background: "white",
              border: "1px solid #ddd",
              borderRadius: "8px",
              boxShadow:
                "0 2px 8px rgba(0,0,0,0.1)",
              zIndex: 1000,
              overflow: "hidden"
            }}
          >

            {suggestions.map(
              (item, index) => (

                <div
                  key={index}
                  style={{
                    padding: "10px",
                    cursor: "pointer",
                    borderBottom:
                      "1px solid #eee",
                    color: "#111827",
                    overflow: "hidden",
                    textOverflow:
                      "ellipsis",
                    whiteSpace:
                      "nowrap"
                  }}
                  title={item}
                  onClick={() => {
                    setSearch(item);
                    setSuggestions([]);
                    searchDocuments(item);
                  }}
                >
                  📄 {item}
                </div>

              )
            )}

          </div>

        )}


        {/* ==========================
            LOADING
        ========================== */}

        {loading && (

          <p
            style={{
              color: "#2563eb",
              fontWeight: "bold",
              marginTop: "10px"
            }}
          >
            🔍 Searching documents...
          </p>

        )}

      </div>


      {/* =====================================================
          NORMAL SEARCH RESULTS
          ===================================================== */}

      {search.trim() !== "" ? (

        <div>

          <h3
            style={{
              marginBottom: "15px",
              color: "#374151"
            }}
          >
            🔍 Search Results
          </h3>

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fill, minmax(300px, 1fr))",
              gap: "20px"
            }}
          >

            {docs.map((doc) => (

              <DocumentCard
                key={doc.id}
                doc={doc}
                onView={openDocument}
                onDelete={deleteDocument}
              />

            ))}

          </div>

          {docs.length === 0 &&
            !loading && (

              <div
                style={{
                  marginTop: "30px",
                  padding: "30px",
                  textAlign: "center",
                  color: "#6b7280",
                  background: "white",
                  borderRadius: "10px"
                }}
              >
                No documents found.
              </div>

          )}

        </div>

      ) : (

        /* =====================================================
           SUBJECT-BASED DOCUMENT VIEW
           ===================================================== */

        <div>

          {groupedDocuments.length === 0 && (

            <div
              style={{
                marginTop: "30px",
                padding: "30px",
                textAlign: "center",
                color: "#6b7280",
                background: "white",
                borderRadius: "10px"
              }}
            >
              No documents found.
            </div>

          )}


          {groupedDocuments.map(
            (group) => {

              const subject =
                group.subject;

              const subjectFiles =
                group.documents || [];

              const isExpanded =
                expandedSubjects[
                  subject
                ];

              return (

                <div
                  key={subject}
                  style={{
                    marginBottom: "15px",
                    background: "white",
                    borderRadius: "12px",
                    boxShadow:
                      "0 2px 10px rgba(0,0,0,0.08)",
                    overflow: "hidden"
                  }}
                >

                  {/* ==========================
                      SUBJECT HEADER
                  ========================== */}

                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      padding: "16px 18px",
                      background:
                        "#f8fafc",
                      borderBottom:
                        isExpanded
                          ? "1px solid #e5e7eb"
                          : "none"
                    }}
                  >

                    {/* EXPAND BUTTON */}

                    <button
                      type="button"
                      onClick={() =>
                        toggleSubject(
                          subject
                        )
                      }
                      style={{
                        width: "32px",
                        height: "32px",
                        border: "none",
                        borderRadius: "6px",
                        background:
                          "#e5e7eb",
                        color: "#111827",
                        cursor: "pointer",
                        fontSize: "16px",
                        fontWeight: "bold",
                        marginRight: "10px",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center"
                      }}
                    >
                      {isExpanded
                        ? "▼"
                        : "▶"}
                    </button>


                    {/* SUBJECT ICON */}

                    <span
                      style={{
                        fontSize: "20px",
                        marginRight: "10px"
                      }}
                    >
                      📚
                    </span>


                    {/* SUBJECT NAME */}

                    <strong
                      style={{
                        color: "#111827",
                        fontSize: "17px"
                      }}
                    >
                      {subject}
                    </strong>


                    {/* FILE COUNT */}

                    <span
                      style={{
                        marginLeft: "auto",
                        color: "#6b7280",
                        fontSize: "13px",
                        fontWeight: "600"
                      }}
                    >
                      {subjectFiles.length}{" "}
                      {subjectFiles.length === 1
                        ? "file"
                        : "files"}
                    </span>

                  </div>


                  {/* ==========================
                      DOCUMENTS
                  ========================== */}

                  {isExpanded && (

                    <div
                      style={{
                        padding: "18px"
                      }}
                    >

                      <div
                        style={{
                          display: "grid",
                          gridTemplateColumns:
                            "repeat(auto-fill, minmax(300px, 1fr))",
                          gap: "20px"
                        }}
                      >

                        {subjectFiles.map(
                          (doc) => (

                            <DocumentCard
                              key={doc.id}
                              doc={doc}
                              onView={
                                openDocument
                              }
                              onDelete={
                                deleteDocument
                              }
                            />

                          )
                        )}

                      </div>

                    </div>

                  )}

                </div>

              );

            }
          )}

        </div>

      )}

    </div>
  );
}


/* ============================================================
   DOCUMENT CARD
   ============================================================ */

function DocumentCard({
  doc,
  onView,
  onDelete
}) {

  return (

    <div
      style={{
        background: "white",
        padding: "20px",
        borderRadius: "12px",
        boxShadow:
          "0 2px 10px rgba(0,0,0,0.1)",
        border:
          "1px solid #e5e7eb",
        minWidth: 0,
        display: "flex",
        flexDirection: "column"
      }}
    >

      {/* ==========================
          DOCUMENT TITLE
      ========================== */}

      <div
        style={{
          height: "54px",
          marginBottom: "12px",
          minWidth: 0
        }}
      >

        <h3
          title={doc.filename}
          style={{
            margin: 0,
            fontSize: "17px",
            lineHeight: "24px",
            color: "#111827",

            overflow: "hidden",
            textOverflow: "ellipsis",

            display:
              "-webkit-box",
            WebkitBoxOrient:
              "vertical",
            WebkitLineClamp: 2,

            wordBreak:
              "break-word"
          }}
        >
          📄 {doc.filename}
        </h3>

      </div>


      {/* ==========================
          SUBJECT
      ========================== */}

      <div
        style={{
          marginBottom: "10px",
          padding: "7px 10px",
          background: "#eff6ff",
          borderRadius: "6px",
          color: "#1d4ed8",
          fontSize: "13px",
          fontWeight: "600",

          overflow: "hidden",
          textOverflow: "ellipsis",
          whiteSpace: "nowrap"
        }}
        title={
          doc.subject ||
          doc.parent_subject ||
          "Uncategorized"
        }
      >
        📚{" "}
        {doc.subject ||
          doc.parent_subject ||
          "Uncategorized"}
      </div>


      {/* ==========================
          STATUS
      ========================== */}

      <p
        style={{
          margin: "6px 0",
          color: "#374151"
        }}
      >
        <strong>
          Status:
        </strong>{" "}
        {doc.status}
      </p>


      {/* ==========================
          CHUNKS
      ========================== */}

      <p
        style={{
          margin: "6px 0",
          color: "#374151"
        }}
      >
        <strong>
          Chunks:
        </strong>{" "}
        {doc.chunk_count}
      </p>


      {/* ==========================
          UPLOADED DATE
      ========================== */}

      <p
        style={{
          margin: "6px 0 18px",
          color: "#374151"
        }}
      >
        <strong>
          Uploaded:
        </strong>{" "}
        {doc.created_at
          ? new Date(
              doc.created_at
            ).toLocaleDateString()
          : "-"}
      </p>


      {/* ==========================
          BUTTONS
      ========================== */}

      <div
        style={{
          display: "flex",
          gap: "10px",
          marginTop: "auto"
        }}
      >

        {/* VIEW */}

        <button
          type="button"
          onClick={() =>
            onView(doc.id)
          }
          style={{
            background:
              "#2563eb",
            color: "white",
            border: "none",
            padding:
              "10px 15px",
            borderRadius: "8px",
            cursor: "pointer",
            flex: 1
          }}
        >
          View
        </button>


        {/* DELETE */}

        <button
          type="button"
          onClick={() =>
            onDelete(doc.id)
          }
          style={{
            background:
              "#dc3545",
            color: "white",
            border: "none",
            padding:
              "10px 15px",
            borderRadius: "8px",
            cursor: "pointer",
            flex: 1
          }}
        >
          Delete
        </button>

      </div>

    </div>

  );
}
import { useEffect, useState, useRef } from "react";
import { api } from "../api/api";
import AnswerCard from "../components/AnswerCard";
import SourceList from "../components/SourceList";

export default function Ask() {
  const [question, setQuestion] = useState("");

  const [marks, setMarks] = useState(5);

  const [groupedDocuments, setGroupedDocuments] = useState([]);

  const [selectedDocuments, setSelectedDocuments] = useState([]);

  const [expandedSubjects, setExpandedSubjects] = useState({});

  const [documentSelectorOpen, setDocumentSelectorOpen] =
    useState(false);

  const selectorRef = useRef(null);

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState({
    answer: ""
  });

  const [confidence, setConfidence] = useState(null);

  const [sources, setSources] = useState([]);

  const [images, setImages] = useState([]);


  // ==========================
  // LOAD GROUPED DOCUMENTS
  // ==========================

  useEffect(() => {
    api.get("/documents/grouped")
      .then((res) => {
        setGroupedDocuments(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);


  // ==========================
  // CLOSE SELECTOR ON OUTSIDE CLICK
  // ==========================

  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (
        selectorRef.current &&
        !selectorRef.current.contains(event.target)
      ) {
        setDocumentSelectorOpen(false);
      }
    };

    document.addEventListener(
      "mousedown",
      handleOutsideClick
    );

    return () => {
      document.removeEventListener(
        "mousedown",
        handleOutsideClick
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
  // TOGGLE INDIVIDUAL FILE
  // ==========================

  const handleFileToggle = (filename) => {
    setSelectedDocuments((prev) => {
      if (prev.includes(filename)) {
        return prev.filter(
          (file) => file !== filename
        );
      }

      return [
        ...prev,
        filename
      ];
    });
  };


  // ==========================
  // TOGGLE ALL FILES IN SUBJECT
  // ==========================

  const handleSubjectToggle = (subject) => {
    const subjectFiles =
      groupedDocuments.find(
        (group) =>
          group.subject === subject
      )?.documents || [];

    const filenames =
      subjectFiles.map(
        (doc) => doc.filename
      );

    const allSelected =
      filenames.length > 0 &&
      filenames.every(
        (filename) =>
          selectedDocuments.includes(filename)
      );

    setSelectedDocuments((prev) => {
      if (allSelected) {
        return prev.filter(
          (filename) =>
            !filenames.includes(filename)
        );
      }

      return [
        ...new Set([
          ...prev,
          ...filenames
        ])
      ];
    });
  };


  // ==========================
  // ASK QUESTION
  // ==========================

  const handleAsk = async () => {
    if (!question.trim()) {
      alert("Please enter a question");
      return;
    }

    setLoading(true);

    try {
      const res = await api.post(
        "/ask",
        {
          question,
          marks,
          documents: selectedDocuments
        }
      );

      setResult(res.data);

      setSources(
        res.data.sources || []
      );

      setConfidence(
        res.data.confidence
      );

      setImages(
        res.data.images || []
      );

    } catch (err) {
      console.log(err);

      setResult({
        answer: "Error generating answer"
      });

      setImages([]);

      setConfidence(null);

      setSources([]);

    } finally {
      setLoading(false);
    }
  };


  // ==========================
  // TOTAL DOCUMENT COUNT
  // ==========================

  const totalDocuments =
    groupedDocuments.reduce(
      (total, group) =>
        total +
        (group.documents?.length || 0),
      0
    );


  return (
    <div className="page-card">

      <h2>
        Ask Question
      </h2>


      {/* ==========================
          QUESTION
      ========================== */}

      <textarea
        rows="5"
        placeholder="Enter your question..."
        value={question}
        onChange={(e) =>
          setQuestion(
            e.target.value
          )
        }
      />


      <br />
      <br />


      {/* ==========================
          MARKS
      ========================== */}

      <label>
        Marks:
      </label>

      <br />

      <select
        value={marks}
        onChange={(e) =>
          setMarks(
            Number(
              e.target.value
            )
          )
        }
      >
        <option value={2}>
          2 Marks
        </option>

        <option value={5}>
          5 Marks
        </option>

        <option value={10}>
          10 Marks
        </option>
      </select>


      <br />
      <br />


      {/* ==========================
          DOCUMENT SELECTOR
      ========================== */}

      <label>
        Select Document(s)
      </label>

      <br />

      <div
        ref={selectorRef}
        style={{
          position: "relative",
          width: "100%",
          maxWidth: "600px",
          marginTop: "8px"
        }}
      >

        {/* SELECT DOCUMENTS BUTTON */}

        <button
          type="button"
          onClick={() =>
            setDocumentSelectorOpen(
              (prev) => !prev
            )
          }
          style={{
            width: "100%",
            padding: "12px 15px",
            background: "white",
            color: "#111827",
            border: "1px solid #d1d5db",
            borderRadius: "8px",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            fontSize: "15px",
            textAlign: "left"
          }}
        >

          <span>
            {selectedDocuments.length > 0
              ? `${selectedDocuments.length} document${
                  selectedDocuments.length > 1
                    ? "s"
                    : ""
                } selected`
              : "Select Documents"}
          </span>

          <span
            style={{
              fontSize: "14px",
              color: "#374151"
            }}
          >
            {documentSelectorOpen
              ? "▲"
              : "▼"}
          </span>

        </button>


        {/* ==========================
            DROPDOWN PANEL
        ========================== */}

        {documentSelectorOpen && (

          <div
            style={{
              position: "absolute",
              top: "48px",
              left: "0",
              right: "0",
              background: "white",
              border: "1px solid #d1d5db",
              borderRadius: "10px",
              boxShadow:
                "0 8px 20px rgba(0,0,0,0.12)",
              zIndex: 1000,
              maxHeight: "420px",
              overflowY: "auto"
            }}
          >

            {/* PANEL HEADER */}

            <div
              style={{
                padding: "12px 15px",
                borderBottom:
                  "1px solid #e5e7eb",
                fontWeight: "bold",
                color: "#111827",
                display: "flex",
                justifyContent: "space-between"
              }}
            >

              <span>
                Select Documents
              </span>

              <span
                style={{
                  color: "#6b7280",
                  fontSize: "13px",
                  fontWeight: "normal"
                }}
              >
                {totalDocuments} files
              </span>

            </div>


            {/* NO DOCUMENTS */}

            {groupedDocuments.length === 0 && (

              <p
                style={{
                  padding: "20px",
                  color: "#6b7280"
                }}
              >
                No documents available.
              </p>

            )}


            {/* SUBJECT GROUPS */}

            {groupedDocuments.map(
              (group) => {

                const subjectFiles =
                  group.documents || [];

                const filenames =
                  subjectFiles.map(
                    (doc) =>
                      doc.filename
                  );

                const allSelected =
                  filenames.length > 0 &&
                  filenames.every(
                    (filename) =>
                      selectedDocuments.includes(
                        filename
                      )
                  );

                const someSelected =
                  filenames.some(
                    (filename) =>
                      selectedDocuments.includes(
                        filename
                      )
                  );

                return (

                  <div
                    key={group.subject}
                    style={{
                      borderBottom:
                        "1px solid #f1f5f9"
                    }}
                  >

                    {/* SUBJECT HEADER */}

                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        padding: "11px 12px",
                        background:
                          "#f8fafc"
                      }}
                    >

                      {/* EXPAND BUTTON */}

                      <button
                        type="button"
                        onClick={() =>
                          toggleSubject(
                            group.subject
                          )
                        }
                        style={{
                          border: "none",
                          background:
                            "transparent",
                          color: "#111827",
                          cursor: "pointer",
                          fontSize: "15px",
                          fontWeight: "bold",
                          marginRight: "5px",
                          padding: "2px 6px"
                        }}
                      >
                        {expandedSubjects[
                          group.subject
                        ]
                          ? "▼"
                          : "▶"}
                      </button>


                      {/* SUBJECT CHECKBOX */}

                      <input
                        type="checkbox"
                        checked={
                          allSelected
                        }
                        ref={(element) => {
                          if (element) {
                            element.indeterminate =
                              someSelected &&
                              !allSelected;
                          }
                        }}
                        onChange={() =>
                          handleSubjectToggle(
                            group.subject
                          )
                        }
                        style={{
                          marginRight:
                            "10px",
                          cursor:
                            "pointer"
                        }}
                      />


                      {/* SUBJECT NAME */}

                      <span
                        onClick={() =>
                          toggleSubject(
                            group.subject
                          )
                        }
                        style={{
                          flex: 1,
                          cursor: "pointer",
                          fontWeight: "600",
                          color: "#111827"
                        }}
                      >
                        📚 {group.subject}
                      </span>


                      {/* FILE COUNT */}

                      <span
                        style={{
                          color: "#6b7280",
                          fontSize: "12px"
                        }}
                      >
                        {subjectFiles.length}
                      </span>

                    </div>


                    {/* ==========================
                        FILE LIST
                    ========================== */}

                    {expandedSubjects[
                      group.subject
                    ] && (

                      <div
                        style={{
                          padding:
                            "5px 15px 10px 50px"
                        }}
                      >

                        {subjectFiles.map(
                          (doc) => (

                            <label
                              key={doc.id}
                              style={{
                                display:
                                  "flex",
                                alignItems:
                                  "center",
                                padding:
                                  "8px 5px",
                                cursor:
                                  "pointer",
                                borderRadius:
                                  "6px",
                                color:
                                  "#374151"
                              }}
                            >

                              <input
                                type="checkbox"
                                checked={
                                  selectedDocuments.includes(
                                    doc.filename
                                  )
                                }
                                onChange={() =>
                                  handleFileToggle(
                                    doc.filename
                                  )
                                }
                                style={{
                                  marginRight:
                                    "10px",
                                  cursor:
                                    "pointer"
                                }}
                              />

                              <span
                                style={{
                                  overflow:
                                    "hidden",
                                  textOverflow:
                                    "ellipsis",
                                  whiteSpace:
                                    "nowrap"
                                }}
                                title={
                                  doc.filename
                                }
                              >
                                📄 {doc.filename}
                              </span>

                            </label>

                          )
                        )}

                      </div>

                    )}

                  </div>

                );
              }
            )}


            {/* ==========================
                SELECTION FOOTER
            ========================== */}

            <div
              style={{
                position: "sticky",
                bottom: 0,
                padding: "10px 15px",
                background: "white",
                borderTop:
                  "1px solid #e5e7eb",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between"
              }}
            >

              <span
                style={{
                  fontSize: "13px",
                  color: "#4b5563"
                }}
              >
                {selectedDocuments.length === 0
                  ? "No documents selected"
                  : `${selectedDocuments.length} document${
                      selectedDocuments.length > 1
                        ? "s"
                        : ""
                    } selected`}
              </span>


              {/* CLEAR SELECTION */}

              {selectedDocuments.length > 0 && (

                <button
                  type="button"
                  onClick={() =>
                    setSelectedDocuments([])
                  }
                  style={{
                    border: "none",
                    background:
                      "transparent",
                    color: "#dc2626",
                    cursor: "pointer",
                    fontSize: "13px"
                  }}
                >
                  Clear
                </button>

              )}

            </div>

          </div>

        )}

      </div>


      <br />


      {/* ==========================
          GENERATE ANSWER
      ========================== */}

      <button
        onClick={handleAsk}
        disabled={loading}
      >
        {loading
          ? "🤖 Generating AI Answer..."
          : "Generate Answer"}
      </button>


      {/* ==========================
          LOADING
      ========================== */}

      {loading && (

        <div>

          <div className="spinner">
          </div>

          <p>
            AI is analyzing
            your notes...
          </p>

        </div>

      )}


      {/* ==========================
          CONFIDENCE
      ========================== */}

      {confidence !== null && (

        <div
          style={{
            marginTop: "15px"
          }}
        >

          <strong>
            Confidence:
          </strong>{" "}

          {confidence != null
            ? confidence.toFixed(2)
            : 0
          }%

        </div>

      )}


      {/* ==========================
          ANSWER
      ========================== */}

      <AnswerCard
        answer={
          result?.answer || ""
        }
        confidence={
          confidence
        }
        images={
          images
        }
      />


      {/* ==========================
          SOURCES
      ========================== */}

      <SourceList
        sources={
          sources
        }
      />

    </div>
  );
}
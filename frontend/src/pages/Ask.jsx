import { useEffect, useState } from "react";
import { api } from "../api/api";
import AnswerCard from "../components/AnswerCard";
import SourceList from "../components/SourceList";

export default function Ask() {

  const [question, setQuestion] = useState("");

  const [marks, setMarks] = useState(5);

  const [documents, setDocuments] = useState([]);

  const [selectedDocuments, setSelectedDocuments] =
    useState([]);

  const [loading, setLoading] = useState(false);

  const [answer, setAnswer] = useState("");

  const [confidence, setConfidence] =
    useState(null);

  const [sources, setSources] = useState([]);

  // ==========================
  // LOAD DOCUMENTS
  // ==========================
  useEffect(() => {

    api.get("/documents")
      .then((res) => {

        setDocuments(res.data);

      })
      .catch((err) => {

        console.log(err);

      });

  }, []);

  // ==========================
  // MULTI SELECT
  // ==========================
  const handleDocumentChange = (e) => {

    const values =
      Array.from(
        e.target.selectedOptions,
        option => option.value
      );

    setSelectedDocuments(values);

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
          documents:
            selectedDocuments
        }
      );

      setAnswer(
        res.data.answer
      );

      setSources(
        res.data.sources || []
      );

      setConfidence(
        res.data.confidence
      );

    } catch (err) {

      console.log(err);

      setAnswer(
        "Error generating answer"
      );

    } finally {

      setLoading(false);

    }

  };

  return (

    <div className="page-card">

      <h2>
        Ask Question
      </h2>

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

      <label>
        Select Document(s)
      </label>

      <br />

      <select
        multiple
        size="6"
        value={selectedDocuments}
        onChange={
          handleDocumentChange
        }
        style={{
          width: "100%",
          maxWidth: "600px",
          padding: "10px"
        }}
      >

        {
          documents.map(
            (doc) => (
              <option
                key={doc.id}
                value={
                  doc.filename
                }
              >
                {doc.filename}
              </option>
            )
          )
        }

      </select>

      <p
        style={{
          fontSize: "14px",
          color: "gray"
        }}
      >
        Hold Ctrl (Windows)
        or Cmd (Mac)
        to select multiple files.
      </p>

      <br />

      <button
        onClick={handleAsk}
        disabled={loading}
      >
        {
          loading
            ? "🤖 Generating AI Answer..."
            : "Generate Answer"
        }
      </button>

      {
        loading && (

          <div>

            <div className="spinner">

            </div>

            <p>
              AI is analyzing
              your notes...
            </p>

          </div>

        )
      }

      {
        confidence !== null && (

          <div
            style={{
              marginTop: "15px"
            }}
          >
            <strong>
              Confidence:
            </strong>{" "}
            {
              (
                confidence * 100
              ).toFixed(0)
            }
            %
          </div>

        )
      }

      <AnswerCard
        answer={answer}
        confidence={confidence}
      />

      <SourceList
        sources={sources}
      />

    </div>

  );

}
import { useState } from "react";
import { api } from "../api/api";

export default function Upload() {

  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState("");
  const [documentId, setDocumentId] = useState(null);
  const openExistingDocument = async () => {

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

  }
};
  const handleUpload = async () => {

    if (!file) {
      setMessage("❌ Please select a file");
      return;
    }

    if (uploading) {
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {

      setUploading(true);
      setProgress(0);

      setMessage(
        "Uploading and processing document. Please wait..."
      );

      const res = await api.post(
        "/upload",
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data"
          },

          onUploadProgress: (event) => {

            const percent = Math.round(
              (event.loaded * 100) /
              event.total
            );

            setProgress(percent);
          }
        }
      );

      if (res.data.error) {

        let msg =
    `❌ ${res.data.error}`;

        if (res.data.existing_document) {

    msg +=
      `\n\n📄 Existing File:\n${res.data.existing_document}`;
  }

        if (res.data.similarity) {

    msg +=
      `\n\n🎯 Similarity: ${res.data.similarity}%`;
  }

  setMessage(msg);
  setDocumentId(
  res.data.document_id
);

}      else {

  let msg =`✅ Upload Successful

Original File:
${res.data.original_filename}

Stored As:
${res.data.stored_filename}

Suggested Title:
${res.data.suggested_title}`
;

  if (res.data.warning) {

    msg +=
      `\n\n⚠ ${res.data.warning}`;

    msg +=
      `\n📄 Existing File: ${res.data.existing_document}`;

    msg +=
      `\n🎯 Similarity: ${res.data.similarity}%`;
  }

  setMessage(msg);

  setFile(null);
}

    } catch (err) {

      if (
        err.response &&
        err.response.data &&
        err.response.data.detail
      ) {

        setMessage(
          `❌ ${err.response.data.detail}`
        );

      } else {

        setMessage(
          "❌ Upload failed"
        );
      }

    } finally {

      setUploading(false);

    }
  };

  return (
    <div className="page-container">

      <h1>📄 Upload Document</h1>

      <input
        type="file"
        onChange={(e) =>
          setFile(e.target.files[0])
        }
      />

      {
        file && (
          <p
            style={{
              marginTop: "10px",
              fontSize: "16px"
            }}
          >
            📄 Selected File:
            <strong> {file.name}</strong>
          </p>
        )
      }

      <br />

      <button
        onClick={handleUpload}
        disabled={uploading}
      >
        {
          uploading
            ? "Uploading..."
            : "Upload Document"
        }
      </button>

      {
        uploading && (
          <>
            <br />
            <br />

            <div className="progress-bar">

              <div
                className="progress-fill"
                style={{
                  width: `${progress}%`
                }}
              >
                {progress}%
              </div>

            </div>
          </>
        )
      }

      <br />
      <br />

      {
  message && (

    <div
      style={{
        marginTop: "20px",
        padding: "15px",
        borderRadius: "10px",
        whiteSpace: "pre-line",
        background:
          message.includes("❌")
          ? "#ffe5e5"
          : "#e8f5e9",
        border:
          message.includes("❌")
          ? "1px solid #ff4d4f"
          : "1px solid #4caf50"
      }}
    >
      {message}
    </div>

  )
}
{
  documentId && (

    <button
      onClick={openExistingDocument}
      style={{
        marginTop: "15px",
        background: "#2563eb",
        color: "white",
        border: "none",
        padding: "10px 15px",
        borderRadius: "8px",
        cursor: "pointer"
      }}
    >
      📄 Open Existing Document
    </button>

  )
}

    </div>
  );
}
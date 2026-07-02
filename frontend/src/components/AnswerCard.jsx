export default function AnswerCard({
  answer,
  confidence,
  images = []
}) {
  if (!answer) return null;

  const copyAnswer = () => {
    navigator.clipboard.writeText(
      answer
    );
  };

  return (
    <div className="answer-card">

      <div className="answer-header">

        <h3>🧠 AI Answer</h3>

        <button
          onClick={copyAnswer}
        >
          📋 Copy
        </button>

      </div>

      <p
style={{
color:
confidence > 0.8
? "green"
: confidence > 0.6
? "orange"
: "red"
}}
>
Confidence:
{confidence}
</p>

      <pre>
        {answer}
      </pre>
      {images.length > 0 && (

  <div style={{ marginTop: "25px" }}>

    <h3>Relevant Diagrams</h3>

    {images.map((img, index) => (

      <div
        key={index}
        style={{
          marginBottom: "25px"
        }}
      >

        <img
          src={`http://localhost:8000/${img.image_path}`}
          alt={img.caption}
          style={{
            maxWidth: "100%",
            border: "1px solid #ccc",
            borderRadius: "6px"
          }}
        />

        <p>
          <strong>Page:</strong> {img.page_no}
        </p>

        <p>{img.caption}</p>

      </div>

    ))}

  </div>

)}

    </div>
  );
}

const downloadAnswer = () => {

  const blob = new Blob(
    [answer],
    {
      type: "text/plain"
    }
  );

  const url =
    window.URL.createObjectURL(
      blob
    );

  const a =
    document.createElement("a");

  a.href = url;

  a.download =
    "answer.txt";

  a.click();
};
<button
  onClick={downloadAnswer}
>
  ⬇ Download
</button>

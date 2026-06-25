export default function AnswerCard({
  answer,
  confidence
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

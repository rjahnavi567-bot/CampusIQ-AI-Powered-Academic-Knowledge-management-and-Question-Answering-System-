import jsPDF from "jspdf";

export default function AnswerCard({
  answer,
  confidence,
  images = []
}) {

  if (!answer) return null;

  //------------------------------------
  // Copy Answer
  //------------------------------------

  const copyAnswer = () => {
    navigator.clipboard.writeText(answer);
  };

  //------------------------------------
  // Download PDF
  //------------------------------------

  const downloadAnswer = async () => {

    const pdf = new jsPDF();

    let y = 15;

    pdf.setFontSize(18);
    pdf.text("AI Academic Answer", 10, y);

    y += 10;

    pdf.setFontSize(11);

    const lines = pdf.splitTextToSize(answer, 180);

    pdf.text(lines, 10, y);

    y += lines.length * 6 + 12;

    if (images.length > 0) {

      pdf.setFontSize(15);

      pdf.text("Relevant Diagrams", 10, y);

      y += 10;

      for (const img of images) {

        if (y > 210) {
          pdf.addPage();
          y = 15;
        }

        pdf.setFontSize(13);
        pdf.text(img.title || "Diagram", 10, y);

        y += 7;

        pdf.setFontSize(10);

        pdf.text(`Page : ${img.page_no}`, 10, y);

        y += 6;

        if (img.caption) {
          const captionLines = pdf.splitTextToSize(
            img.caption,
            180
          );

          pdf.text(captionLines, 10, y);

          y += captionLines.length * 5 + 4;
        }

        try {

          const image = new Image();

          image.crossOrigin = "anonymous";

          image.src = `http://localhost:8000/${img.image_path}`;

          await new Promise((resolve, reject) => {

            image.onload = resolve;

            image.onerror = reject;

          });

          const extension =
            img.image_path.toLowerCase().endsWith(".png")
              ? "PNG"
              : "JPEG";

          pdf.addImage(
            image,
            extension,
            10,
            y,
            120,
            80
          );

          y += 90;

        } catch (err) {

          pdf.text("Unable to load image.", 10, y);

          y += 10;

        }

      }

    }

    pdf.save("Academic_Answer.pdf");

  };

  //------------------------------------

  return (

    <div className="answer-card">

      <div className="answer-header">

        <h3>🧠 AI Answer</h3>

        <div>

          <button onClick={copyAnswer}>
            📋 Copy
          </button>

          <button
            style={{ marginLeft: "10px" }}
            onClick={downloadAnswer}
          >
            ⬇ Download PDF
          </button>

        </div>

      </div>

      <p
        style={{
          color:
            confidence > 80
              ? "green"
              : confidence > 60
              ? "orange"
              : "red",
          fontWeight: "bold"
        }}
      >
        Confidence : {confidence}%
      </p>

      <pre
        style={{
          whiteSpace: "pre-wrap",
          lineHeight: "1.6"
        }}
      >
        {answer}
      </pre>

      {images.length > 0 && (

        <>

          <h2 style={{ marginTop: "30px" }}>
            Relevant Diagrams Used For This Answer
          </h2>

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fill,minmax(320px,1fr))",
              gap: "20px",
              marginTop: "20px"
            }}
          >

            {images.map((img, index) => (

              <div
                key={index}
                style={{
                  border: "1px solid #ddd",
                  borderRadius: "10px",
                  padding: "12px",
                  background: "#fff"
                }}
              >

                <img
                  src={`http://localhost:8000/${img.image_path}`}
                  alt={img.title}
                  style={{
                    width: "100%",
                    borderRadius: "8px",
                    marginBottom: "10px"
                  }}
                />

                <h4>{img.title}</h4>

                <p>
                  <b>Page:</b> {img.page_no}
                </p>

                <p>{img.caption}</p>

              </div>

            ))}

          </div>

        </>

      )}

    </div>

  );

}
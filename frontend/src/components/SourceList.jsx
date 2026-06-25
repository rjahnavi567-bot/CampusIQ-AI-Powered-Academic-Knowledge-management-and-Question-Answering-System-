export default function SourceList({
  sources
}) {

  if (!sources?.length) return null;

  return (

    <div className="source-card">

      <h3>
        📚 Sources Used
      </h3>

      <ul>

        {sources.map(
          (s, index) => (

          <li key={index}>
            📄 {s.file}
            {" "}
            (Page {s.page})
          </li>

        ))}

      </ul>

    </div>

  );
}
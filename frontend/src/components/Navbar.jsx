import { Link } from "react-router-dom";

export default function Navbar() {

  return (

    <nav className="navbar">

      <h2>
        🎓 AetherMind: A Context-Aware Academic Intelligence Platform
      </h2>

      <div>

        <Link to="/">
          Dashboard
        </Link>

        <Link to="/upload">
          Upload
        </Link>

        <Link to="/ask">
          Ask
        </Link>
        

        <Link to="/documents">
          Documents
        </Link>


        <Link to="/history">
  History
</Link>
        <Link to="/grouped-history">
  Question Groups
</Link>
      </div>

    </nav>

  );
}
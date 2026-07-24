import {
useEffect,
useState
}
from "react";

import { api }
from "../api/api";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
export default function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [stats,
  setStats] = useState({

    documents:0,

    questions:0,

    recent_questions:[]
  });
  function handleLogout() {

    logout();

    navigate("/login");

}
  useEffect(() => {

  api.get("/dashboard-stats")

    .then((res) => {

      setStats(res.data);

    })

    .catch((err) => {

      console.error(err);

    });

}, []);

  return (

<div className="dashboard">

<div className="hero-card">

<div
    style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center"
    }}
>

    <div>
        <h3>Welcome, {user?.name}</h3>
        <p>{user?.role}</p>
    </div>

    <button onClick={handleLogout}>
        Logout
    </button>

</div>

<h1>
🎓 campusIQ: Intelligent Academic Assistance System
</h1>

<p>
Upload study materials,
generate exam-focused answers,
and learn smarter with AI.
</p>

</div>
<div className="page-card">

  <h3>Welcome, {user?.name}</h3>

  <p>Email: {user?.email}</p>

  <p>Role: {user?.role}</p>

</div>

<div className="stats-grid">

<div className="stat-card">

<h2>📄</h2>

<h3>
{stats.documents}
</h3>

<p>
Documents
</p>

</div>

<div className="stat-card">

<h2>❓</h2>

<h3>
{stats.questions}
</h3>

<p>
Questions Asked
</p>

</div>

</div>

<div
className="page-card"
>

<h2>
Recent Questions
</h2>

<ul
style={{
textAlign:"left"
}}
>

{
stats.recent_questions.map(
(q,index)=>(
<li key={index}>
{q}
</li>
))
}

</ul>

</div>

</div>

  );

}
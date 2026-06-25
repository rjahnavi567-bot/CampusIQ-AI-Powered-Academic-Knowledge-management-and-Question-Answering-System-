import {
useEffect,
useState
}
from "react";

import { api }
from "../api/api";

export default function Dashboard() {

  const [stats,
  setStats] = useState({

    documents:0,

    questions:0,

    recent_questions:[]
  });

  useEffect(()=>{

    api.get(
      "/dashboard-stats"
    )

    .then((res)=>{

      setStats(
        res.data
      );

    });

  },[]);

  return (

<div className="dashboard">

<div className="hero-card">

<h1>
🎓 AI Academic System
</h1>

<p>
Upload study materials,
generate exam-focused
answers,
and learn smarter with AI.
</p>

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
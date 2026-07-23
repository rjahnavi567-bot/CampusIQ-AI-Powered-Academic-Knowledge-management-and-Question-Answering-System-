import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";
import History from "./pages/History";
import Navbar from "./components/Navbar";
import GroupedHistory
from "./pages/GroupedHistory";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import Ask from "./pages/Ask";
import Documents from "./pages/Documents";

function App() {

  return (
    <BrowserRouter>

      <Navbar />

      <Routes>

        <Route
          path="/"
          element={<Dashboard />}
        />

        <Route
          path="/upload"
          element={<Upload />}
        />

        <Route
          path="/ask"
          element={<Ask />}
        />

        <Route
          path="/documents"
          element={<Documents />}
        />

        <Route
  path="/history"
  element={<History />}
/>
        <Route
  path="/grouped-history"
  element={
    <GroupedHistory />
  }
/>
      </Routes>

    </BrowserRouter>
  );
}

export default App;
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";

import { AuthProvider } from "./context/AuthContext";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import Ask from "./pages/Ask";
import Documents from "./pages/Documents";
import History from "./pages/History";
import GroupedHistory from "./pages/GroupedHistory";
import Register from "./pages/Register";
function App() {

  return (

    <AuthProvider>

      <BrowserRouter>

        <Routes>

          {/* ---------------- Login ---------------- */}

          <Route
            path="/login"
            element={<Login />}
          />
          <Route
    path="/register"
    element={<Register />}
/>

          {/* ---------------- Protected Application ---------------- */}

          <Route
            path="/*"
            element={

              <ProtectedRoute>

                <>

                  <Navbar />

                  <Routes>

                    <Route
                      path="/"
                      element={<Navigate to="/dashboard" replace />}
                    />

                    <Route
                      path="/dashboard"
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
                      element={<GroupedHistory />}
                    />

                  </Routes>

                </>

              </ProtectedRoute>

            }
          />

        </Routes>

      </BrowserRouter>

    </AuthProvider>

  );

}

export default App;
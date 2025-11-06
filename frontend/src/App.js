import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import {
  Company,
  Departments,
  Employees,
  Home,
  Login,
  Profile,
  RPE,
  Teams,
} from "./pages";

import { Header, Footer } from "./components";
import "./index.css";
import { createContext, useState } from "react";

export const UserContext = createContext(null);

export default function App() {
  const [user, setUser] = useState(() => {
    const stored = sessionStorage.getItem("user");
    return stored ? JSON.parse(stored) : null;
  });

  const role = user?._role || "";

  return (
    <UserContext.Provider value={{ user, setUser }}>
      <Router>
        <div className="router">
          <Header />
          <div className="page-container">
            <Routes>
              {!role && (
                <>
                  <Route path="/login" element={<Login />} />
                  <Route path="*" element={<Login />} />
                </>
              )}
              {role === "Director" && (
                <>
                  <Route path="/" element={<Home />} />
                  <Route path="/profile" element={<Profile />} />
                  <Route path="/company" element={<Company />} />
                  <Route path="/departments" element={<Departments />} />
                  <Route path="/employees" element={<Employees />} />
                  <Route path="/teams" element={<Teams />} />
                  <Route path="/rpe" element={<RPE />} />
                  <Route path="*" element={<h2>Page Not Found</h2>} />
                </>
              )}
              {role === "Manager" && (
                <>
                  <Route path="/" element={<Home />} />
                  <Route path="/profile" element={<Profile />} />
                  <Route path="/teams" element={<Teams />} />
                  <Route path="/rpe" element={<RPE />} />
                  <Route path="*" element={<h2>Page Not Found</h2>} />
                </>
              )}
              {role === "Employee" && (
                <>
                  <Route path="/" element={<Home />} />
                  <Route path="/profile" element={<Profile />} />
                  <Route path="*" element={<h2>Page Not Found</h2>} />
                </>
              )}
            </Routes>
          </div>
          <Footer />
        </div>
      </Router>
    </UserContext.Provider>
  );
}

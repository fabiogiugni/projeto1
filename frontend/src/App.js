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

export default function App() {
  return (
    <Router>
      <div className="router">
        <Header />
        <div className="page-container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/company" element={<Company />} />
            <Route path="/departments" element={<Departments />} />
            <Route path="/employees" element={<Employees />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/rpe" element={<RPE />} />
            <Route path="*" element={<h2>Page Not Found</h2>} />
          </Routes>
        </div>
        <Footer />
      </div>
    </Router>
  );
}

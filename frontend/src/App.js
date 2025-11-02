import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { 
  Company, 
  Departments, 
  Employees, 
  Home, 
  Login, 
  Profile, 
  RPE, 
  Teams 
} from "./pages"; 

import {Header} from "./components"


export default function App() {
  return (
    <Router>
      <Header/>
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
    </Router>
  );
}

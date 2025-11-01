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

export default function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/profile">Profile</Link></li>
            <li><Link to="/company">Company</Link></li>
            <li><Link to="/departments">Departments</Link></li>
            <li><Link to="/employees">Employees</Link></li>
            <li><Link to="/teams">Teams</Link></li>
            <li><Link to="/rpe">RPE</Link></li>
          </ul>
        </nav>

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
    </Router>
  );
}

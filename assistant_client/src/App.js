import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from "react-router-dom";
import '../node_modules/bootstrap/dist/css/bootstrap.min.css'
import Login from './pages/Login';
import Home from './pages/Home';
import Connections from './pages/Connections';
import Projects from './pages/Projects';
import ProtectedRoute from './components/ProtectedRoute';
import Results from './pages/Results';
import NotFound from './pages/NotFound';

function Logout(){
  localStorage.clear()
  return <Navigate to="/login"/>
}


function App() {
  return (
    <Router>
      <div className='App'>
      <nav className="navbar navbar-expand-lg navbar-light fixed-top bg-light">
          <div className="container">
            <ul className="navbar-nav mr-auto">
              <li className="nav-item">
                <Link to="/" className="nav-link">Home</Link>
              </li>
              <li className="nav-item">
                <Link to="/login" className="nav-link">Login</Link>
              </li>
              <li className="nav-item">
                <Link to="/projects" className="nav-link">Projects</Link>
              </li>
              <li className="nav-item">
                <Link to="/settings" className="nav-link">Settings</Link>
              </li>
            </ul>
          </div>
        </nav>
        <Routes>
          <Route path="/" element={
            <Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/projects" element={
              <Projects/>
          }/>
          <Route path="/results" element={
              <Results/>
          }/>
          <Route path="/settings" element={
              <Connections/>
          }/>
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </Router>
  );
}


export default App;

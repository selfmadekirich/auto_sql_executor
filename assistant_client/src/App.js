import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from "react-router-dom";
import '../node_modules/bootstrap/dist/css/bootstrap.min.css'
import Login from './pages/Login';
import Home from './pages/Home';
import Connections from './pages/Connections';
import ProtectedRoute from './components/ProtectedRoute';
import NotFound from './pages/NotFound';

function Logout(){
  localStorage.clear()
  return <Navigate to="/login"/>
}


function App() {
  return (
    <Router>
      <div className='App'>
        <nav className="navbar navbar-expand-lg navbar-light fixed-top">
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/login">Login</Link>
            </li>
          </ul>
        </nav>
        <div className="auth-wrapper">
        <div className="auth-inner">
        <Routes>
          <Route path="/" element={
            <Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/projects" element={
            <ProtectedRoute> 
              <Connections/>
            </ProtectedRoute>
          }/>
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
      </div>
      </div>
    </Router>
  );
}


export default App;

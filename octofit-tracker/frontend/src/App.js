import './App.css';
import { Routes, Route, NavLink } from 'react-router-dom';
import octofitLogo from './octofitapp-small.png';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

const navItems = [
  { to: '/users',       label: 'Users',       icon: '👤' },
  { to: '/teams',       label: 'Teams',       icon: '🏆' },
  { to: '/activities',  label: 'Activities',  icon: '🏃' },
  { to: '/leaderboard', label: 'Leaderboard', icon: '📊' },
  { to: '/workouts',    label: 'Workouts',    icon: '💪' },
];

function HomePage() {
  return (
    <div className="container py-5">
      {/* Hero banner */}
      <div className="hero-section text-center mb-5">
        <div style={{ fontSize: '3.5rem', lineHeight: 1 }}>🐙</div>
        <h1 className="mt-3">Welcome to OctoFit Tracker</h1>
        <p className="lead mt-2 mb-4">
          Log activities, join teams, and compete on the leaderboard!
        </p>
        <NavLink className="btn btn-light btn-lg fw-semibold px-4" to="/activities">
          Get Started
        </NavLink>
      </div>

      {/* Feature nav cards */}
      <div className="row g-3 justify-content-center">
        {navItems.map((item) => (
          <div className="col-6 col-sm-4 col-md-2" key={item.to}>
            <NavLink to={item.to} className="hero-nav-card card text-center p-3 d-block">
              <div style={{ fontSize: '2rem' }}>{item.icon}</div>
              <div className="mt-2 fw-semibold small text-primary">{item.label}</div>
            </NavLink>
          </div>
        ))}
      </div>
    </div>
  );
}

function App() {
  return (
    <div className="App">
      {/* ===== Navigation ===== */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark octofit-navbar">
        <div className="container-fluid">
          <NavLink className="navbar-brand d-flex align-items-center gap-2" to="/">
            <img src={octofitLogo} alt="OctoFit" className="octofit-nav-logo" />
            <span>OctoFit Tracker</span>
          </NavLink>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              {navItems.map((item) => (
                <li className="nav-item" key={item.to}>
                  <NavLink
                    className={({ isActive }) =>
                      'nav-link px-3' + (isActive ? ' active' : '')
                    }
                    to={item.to}
                  >
                    {item.icon} {item.label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </nav>

      {/* ===== Main content ===== */}
      <main className="page-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/users"       element={<Users />} />
          <Route path="/teams"       element={<Teams />} />
          <Route path="/activities"  element={<Activities />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/workouts"    element={<Workouts />} />
        </Routes>
      </main>

      {/* ===== Footer ===== */}
      <footer className="bg-dark text-secondary text-center py-3 small">
        &copy; {new Date().getFullYear()} OctoFit Tracker &mdash; Built with 🐙
      </footer>
    </div>
  );
}

export default App;

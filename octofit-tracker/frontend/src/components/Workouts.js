import React, { useState, useEffect } from 'react';

const difficultyBadge = (level) => {
  switch ((level || '').toLowerCase()) {
    case 'easy':   return <span className="badge bg-success">Easy</span>;
    case 'medium': return <span className="badge bg-warning text-dark">Medium</span>;
    case 'hard':   return <span className="badge bg-danger">Hard</span>;
    default:       return <span className="badge bg-secondary">{level || '—'}</span>;
  }
};

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;

  useEffect(() => {
    console.log('Workouts: fetching from REST API endpoint:', apiUrl);
    fetch(apiUrl)
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
      })
      .then((data) => {
        console.log('Workouts: fetched data:', data);
        setWorkouts(Array.isArray(data) ? data : data.results || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Workouts: error fetching data:', err);
        setError(err.message);
        setLoading(false);
      });
  }, [apiUrl]);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="text-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-2 text-muted">Loading workouts&hellip;</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger d-flex align-items-center" role="alert">
          <span className="me-2">&#9888;</span>
          <span><strong>Error:</strong> {error}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="card octofit-card">
        <div className="card-header d-flex align-items-center gap-2">
          <span style={{ fontSize: '1.3rem' }}>💪</span>
          <h2 className="mb-0">Workouts</h2>
          <span className="badge bg-light text-dark ms-auto">{workouts.length}</span>
        </div>
        <div className="card-body p-0">
          <div className="table-responsive">
            <table className="table table-striped table-bordered table-hover octofit-table mb-0">
              <thead className="table-dark">
                <tr>
                  <th>#</th>
                  <th>Workout Name</th>
                  <th>Description</th>
                  <th>Duration (min)</th>
                  <th>Difficulty</th>
                </tr>
              </thead>
              <tbody>
                {workouts.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="text-center text-muted py-4">
                      No workouts found.
                    </td>
                  </tr>
                ) : (
                  workouts.map((workout, index) => (
                    <tr key={workout._id || index}>
                      <td className="text-muted">{index + 1}</td>
                      <td className="fw-semibold">💪 {workout.name}</td>
                      <td>{workout.description || <span className="text-muted">—</span>}</td>
                      <td>
                        <span className="badge bg-info text-dark">
                          {workout.duration} min
                        </span>
                      </td>
                      <td>{difficultyBadge(workout.difficulty)}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Workouts;

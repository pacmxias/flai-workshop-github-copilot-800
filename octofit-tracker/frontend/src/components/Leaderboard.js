import React, { useState, useEffect } from 'react';

const rankBadge = (rank) => {
  if (rank === 1) return <span className="badge rank-gold fs-6">🥇 1st</span>;
  if (rank === 2) return <span className="badge rank-silver fs-6">🥈 2nd</span>;
  if (rank === 3) return <span className="badge rank-bronze fs-6">🥉 3rd</span>;
  return <span className="badge bg-secondary">#{rank}</span>;
};

function Leaderboard() {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;

  useEffect(() => {
    console.log('Leaderboard: fetching from REST API endpoint:', apiUrl);
    fetch(apiUrl)
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
      })
      .then((data) => {
        console.log('Leaderboard: fetched data:', data);
        setEntries(Array.isArray(data) ? data : data.results || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Leaderboard: error fetching data:', err);
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
          <p className="mt-2 text-muted">Loading leaderboard&hellip;</p>
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
          <span style={{ fontSize: '1.3rem' }}>📊</span>
          <h2 className="mb-0">Leaderboard</h2>
          <span className="badge bg-light text-dark ms-auto">{entries.length} players</span>
        </div>
        <div className="card-body p-0">
          <div className="table-responsive">
            <table className="table table-striped table-bordered table-hover octofit-table mb-0">
              <thead className="table-dark">
                <tr>
                  <th>Rank</th>
                  <th>User</th>
                  <th>Team</th>
                  <th>Calories</th>
                  <th>Distance (km)</th>
                  <th>Duration (min)</th>
                  <th>Activities</th>
                </tr>
              </thead>
              <tbody>
                {entries.length === 0 ? (
                  <tr>
                    <td colSpan="7" className="text-center text-muted py-4">
                      No leaderboard entries found.
                    </td>
                  </tr>
                ) : (
                  entries.map((entry, index) => (
                    <tr
                      key={entry._id || index}
                      className={entry.rank <= 3 ? 'table-warning' : ''}
                    >
                      <td>{rankBadge(entry.rank)}</td>
                      <td className="fw-semibold">{entry.user_name}</td>
                      <td>{entry.team_name || <span className="text-muted">—</span>}</td>
                      <td>
                        <span className="badge bg-danger bg-opacity-10 text-danger border border-danger border-opacity-25">
                          {entry.total_calories} kcal
                        </span>
                      </td>
                      <td>{entry.total_distance} km</td>
                      <td>{entry.total_duration} min</td>
                      <td>
                        <span className="badge bg-primary">{entry.total_activities}</span>
                      </td>
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

export default Leaderboard;

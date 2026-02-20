import React, { useState, useEffect } from 'react';

const roleBadgeClass = (role) => {
  switch ((role || '').toLowerCase()) {
    case 'admin':   return 'bg-danger';
    case 'coach':   return 'bg-warning text-dark';
    default:        return 'bg-secondary';
  }
};

function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;

  useEffect(() => {
    console.log('Users: fetching from REST API endpoint:', apiUrl);
    fetch(apiUrl)
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
      })
      .then((data) => {
        console.log('Users: fetched data:', data);
        setUsers(Array.isArray(data) ? data : data.results || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Users: error fetching data:', err);
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
          <p className="mt-2 text-muted">Loading users&hellip;</p>
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
          <span style={{ fontSize: '1.3rem' }}>👤</span>
          <h2 className="mb-0">Users</h2>
          <span className="badge bg-light text-dark ms-auto">{users.length}</span>
        </div>
        <div className="card-body p-0">
          <div className="table-responsive">
            <table className="table table-striped table-bordered table-hover octofit-table mb-0">
              <thead className="table-dark">
                <tr>
                  <th>#</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Team</th>
                  <th>Role</th>
                  <th>Joined</th>
                </tr>
              </thead>
              <tbody>
                {users.length === 0 ? (
                  <tr>
                    <td colSpan="6" className="text-center text-muted py-4">
                      No users found.
                    </td>
                  </tr>
                ) : (
                  users.map((user, index) => (
                    <tr key={user._id || index}>
                      <td className="text-muted">{index + 1}</td>
                      <td className="fw-semibold">{user.name}</td>
                      <td>
                        <a href={`mailto:${user.email}`} className="text-decoration-none">
                          {user.email}
                        </a>
                      </td>
                      <td>{user.team_name || <span className="text-muted">—</span>}</td>
                      <td>
                        <span className={`badge ${roleBadgeClass(user.role)}`}>
                          {user.role || 'member'}
                        </span>
                      </td>
                      <td className="text-nowrap">
                        {user.created_at ? new Date(user.created_at).toLocaleDateString() : '—'}
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

export default Users;

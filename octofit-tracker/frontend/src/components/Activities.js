import React, { useState, useEffect } from 'react';

const activityIcon = (type) => {
  switch ((type || '').toLowerCase()) {
    case 'running':   return '🏃';
    case 'cycling':   return '🚴';
    case 'swimming':  return '🏊';
    case 'walking':   return '🚶';
    case 'hiking':    return '🥾';
    case 'yoga':      return '🧘';
    default:          return '⚡';
  }
};

function Activities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`;

  useEffect(() => {
    console.log('Activities: fetching from REST API endpoint:', apiUrl);
    fetch(apiUrl)
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
      })
      .then((data) => {
        console.log('Activities: fetched data:', data);
        setActivities(Array.isArray(data) ? data : data.results || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Activities: error fetching data:', err);
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
          <p className="mt-2 text-muted">Loading activities&hellip;</p>
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
          <span style={{ fontSize: '1.3rem' }}>🏃</span>
          <h2 className="mb-0">Activities</h2>
          <span className="badge bg-light text-dark ms-auto">{activities.length}</span>
        </div>
        <div className="card-body p-0">
          <div className="table-responsive">
            <table className="table table-striped table-bordered table-hover octofit-table mb-0">
              <thead className="table-dark">
                <tr>
                  <th>#</th>
                  <th>User</th>
                  <th>Type</th>
                  <th>Duration (min)</th>
                  <th>Distance (km)</th>
                  <th>Calories</th>
                  <th>Date</th>
                  <th>Notes</th>
                </tr>
              </thead>
              <tbody>
                {activities.length === 0 ? (
                  <tr>
                    <td colSpan="8" className="text-center text-muted py-4">
                      No activities found.
                    </td>
                  </tr>
                ) : (
                  activities.map((activity, index) => (
                    <tr key={activity._id || index}>
                      <td className="text-muted">{index + 1}</td>
                      <td className="fw-semibold">{activity.user_name}</td>
                      <td>
                        <span className="me-1">{activityIcon(activity.activity_type)}</span>
                        <span className="badge bg-primary bg-opacity-10 text-primary border border-primary border-opacity-25">
                          {activity.activity_type}
                        </span>
                      </td>
                      <td>{activity.duration}</td>
                      <td>{activity.distance}</td>
                      <td>
                        <span className="badge bg-success bg-opacity-10 text-success border border-success border-opacity-25">
                          {activity.calories} kcal
                        </span>
                      </td>
                      <td className="text-nowrap">
                        {activity.date ? new Date(activity.date).toLocaleDateString() : '—'}
                      </td>
                      <td className="text-muted fst-italic">{activity.notes || '—'}</td>
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

export default Activities;

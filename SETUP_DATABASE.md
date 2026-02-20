# OctoFit Tracker - Database Setup Instructions

This guide will help you set up and populate the OctoFit database with test data.

## Prerequisites

- MongoDB service is running (already verified)
- Python virtual environment exists at `octofit-tracker/backend/venv`
- All required packages are installed

## Quick Setup

Run all setup commands in one go:

```bash
cd /workspaces/flai-workshop-github-copilot-800
bash run_setup.sh
```

Or run commands individually:

```bash
cd /workspaces/flai-workshop-github-copilot-800

# Run migrations
./octofit-tracker/backend/venv/bin/python octofit-tracker/backend/manage.py makemigrations octofit_tracker
./octofit-tracker/backend/venv/bin/python octofit-tracker/backend/manage.py migrate

# Populate database with test data
./octofit-tracker/backend/venv/bin/python octofit-tracker/backend/manage.py populate_db

# Verify database
./octofit-tracker/backend/venv/bin/python octofit-tracker/backend/verify_db.py
```

## Verify with mongosh

You can also verify the database manually using mongosh:

```bash
# Connect to MongoDB
mongosh

# Switch to octofit_db
use octofit_db

# List all collections
show collections

# View sample data from each collection
db.users.findOne()
db.teams.findOne()
db.activities.findOne()
db.leaderboard.findOne()
db.workouts.findOne()

# Count documents in each collection
db.users.countDocuments()
db.teams.countDocuments()
db.activities.countDocuments()
db.leaderboard.countDocuments()
db.workouts.countDocuments()

# Exit mongosh
exit
```

## What Gets Created

### Collections:
1. **users** - 10 superhero users (5 from Team Marvel, 5 from Team DC)
2. **teams** - 2 teams (Team Marvel and Team DC)
3. **activities** - 50-100 activity records with various types
4. **leaderboard** - Ranked leaderboard entries for all users
5. **workouts** - 6 workout recommendations with different difficulty levels

### API Endpoints:
Once populated, the following REST API endpoints will be available:

- `http://localhost:8000/api/users/`
- `http://localhost:8000/api/teams/`
- `http://localhost:8000/api/activities/`
- `http://localhost:8000/api/leaderboard/`
- `http://localhost:8000/api/workouts/`

## Troubleshooting

### If migrations fail:
```bash
# Delete the migrations folder and try again
rm -rf octofit-tracker/backend/octofit_tracker/migrations
./octofit-tracker/backend/venv/bin/python octofit-tracker/backend/manage.py makemigrations octofit_tracker
./octofit-tracker/backend/venv/bin/python octofit-tracker/backend/manage.py migrate
```

### If database population fails:
```bash
# Drop the database and try again
mongosh --eval "use octofit_db; db.dropDatabase()"
./octofit-tracker/backend/venv/bin/python octofit-tracker/backend/manage.py populate_db
```

### Check MongoDB service:
```bash
ps aux | grep mongod
```

## Start the Django Server

After setup, start the Django development server:

```bash
cd /workspaces/flai-workshop-github-copilot-800
./octofit-tracker/backend/venv/bin/python octofit-tracker/backend/manage.py runserver 0.0.0.0:8000
```

The API will be available at `http://localhost:8000/api/`

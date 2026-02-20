from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email field
        self.stdout.write('Creating unique index on email field...')
        db.users.create_index('email', unique=True)

        # Create teams
        self.stdout.write('Creating teams...')
        teams = [
            {
                'name': 'Team Marvel',
                'description': 'Earth\'s Mightiest Heroes',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Team DC',
                'description': 'Justice League United',
                'created_at': datetime.utcnow()
            }
        ]
        team_results = db.teams.insert_many(teams)
        team_marvel_id = str(team_results.inserted_ids[0])
        team_dc_id = str(team_results.inserted_ids[1])

        # Create users (superheroes)
        self.stdout.write('Creating superhero users...')
        users = [
            # Team Marvel
            {
                'name': 'Tony Stark',
                'email': 'ironman@marvel.com',
                'password': 'hashed_password',
                'team_id': team_marvel_id,
                'team_name': 'Team Marvel',
                'role': 'Genius, Billionaire, Playboy, Philanthropist',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Steve Rogers',
                'email': 'captainamerica@marvel.com',
                'password': 'hashed_password',
                'team_id': team_marvel_id,
                'team_name': 'Team Marvel',
                'role': 'Super Soldier',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Natasha Romanoff',
                'email': 'blackwidow@marvel.com',
                'password': 'hashed_password',
                'team_id': team_marvel_id,
                'team_name': 'Team Marvel',
                'role': 'Master Spy',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Thor Odinson',
                'email': 'thor@marvel.com',
                'password': 'hashed_password',
                'team_id': team_marvel_id,
                'team_name': 'Team Marvel',
                'role': 'God of Thunder',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Bruce Banner',
                'email': 'hulk@marvel.com',
                'password': 'hashed_password',
                'team_id': team_marvel_id,
                'team_name': 'Team Marvel',
                'role': 'Scientist',
                'created_at': datetime.utcnow()
            },
            # Team DC
            {
                'name': 'Clark Kent',
                'email': 'superman@dc.com',
                'password': 'hashed_password',
                'team_id': team_dc_id,
                'team_name': 'Team DC',
                'role': 'Man of Steel',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Bruce Wayne',
                'email': 'batman@dc.com',
                'password': 'hashed_password',
                'team_id': team_dc_id,
                'team_name': 'Team DC',
                'role': 'Dark Knight',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Diana Prince',
                'email': 'wonderwoman@dc.com',
                'password': 'hashed_password',
                'team_id': team_dc_id,
                'team_name': 'Team DC',
                'role': 'Amazon Warrior',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Barry Allen',
                'email': 'flash@dc.com',
                'password': 'hashed_password',
                'team_id': team_dc_id,
                'team_name': 'Team DC',
                'role': 'Fastest Man Alive',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Arthur Curry',
                'email': 'aquaman@dc.com',
                'password': 'hashed_password',
                'team_id': team_dc_id,
                'team_name': 'Team DC',
                'role': 'King of Atlantis',
                'created_at': datetime.utcnow()
            }
        ]
        user_results = db.users.insert_many(users)
        user_ids = [str(uid) for uid in user_results.inserted_ids]

        # Create activities
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weight Training', 'Yoga', 'Boxing']
        activities = []
        
        for i, user_id in enumerate(user_ids):
            user_email = users[i]['email']
            user_name = users[i]['name']
            team_id = users[i]['team_id']
            
            # Create 5-10 activities per user
            num_activities = random.randint(5, 10)
            for j in range(num_activities):
                activity = {
                    'user_id': user_id,
                    'user_email': user_email,
                    'user_name': user_name,
                    'team_id': team_id,
                    'activity_type': random.choice(activity_types),
                    'duration': random.randint(15, 120),  # minutes
                    'distance': round(random.uniform(1.0, 20.0), 2),  # km
                    'calories': random.randint(100, 1000),
                    'date': datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                    'notes': f'Great workout session {j+1}'
                }
                activities.append(activity)
        
        db.activities.insert_many(activities)

        # Create leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        leaderboard = []
        
        for i, user_id in enumerate(user_ids):
            user_activities = [a for a in activities if a['user_id'] == user_id]
            total_calories = sum(a['calories'] for a in user_activities)
            total_distance = sum(a['distance'] for a in user_activities)
            total_duration = sum(a['duration'] for a in user_activities)
            
            leaderboard.append({
                'user_id': user_id,
                'user_email': users[i]['email'],
                'user_name': users[i]['name'],
                'team_id': users[i]['team_id'],
                'team_name': users[i]['team_name'],
                'total_calories': total_calories,
                'total_distance': round(total_distance, 2),
                'total_duration': total_duration,
                'total_activities': len(user_activities),
                'last_updated': datetime.utcnow()
            })
        
        # Sort by total calories
        leaderboard.sort(key=lambda x: x['total_calories'], reverse=True)
        
        # Add rank
        for rank, entry in enumerate(leaderboard, 1):
            entry['rank'] = rank
        
        db.leaderboard.insert_many(leaderboard)

        # Create workout recommendations
        self.stdout.write('Creating workout recommendations...')
        workouts = [
            {
                'name': 'Super Soldier Training',
                'description': 'High-intensity workout for building strength and endurance',
                'duration': 60,
                'difficulty': 'Advanced',
                'exercises': [
                    {'name': 'Push-ups', 'sets': 5, 'reps': 20},
                    {'name': 'Pull-ups', 'sets': 5, 'reps': 15},
                    {'name': 'Squats', 'sets': 5, 'reps': 25},
                    {'name': 'Burpees', 'sets': 4, 'reps': 15}
                ],
                'category': 'Strength',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Speed Force Training',
                'description': 'Cardiovascular workout for maximum speed and agility',
                'duration': 45,
                'difficulty': 'Advanced',
                'exercises': [
                    {'name': 'Sprint Intervals', 'duration': '10 minutes'},
                    {'name': 'Jump Rope', 'duration': '5 minutes'},
                    {'name': 'Ladder Drills', 'duration': '10 minutes'},
                    {'name': 'Box Jumps', 'sets': 4, 'reps': 15}
                ],
                'category': 'Cardio',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Amazon Warrior Workout',
                'description': 'Full-body combat training for strength and flexibility',
                'duration': 75,
                'difficulty': 'Advanced',
                'exercises': [
                    {'name': 'Sword Training', 'duration': '15 minutes'},
                    {'name': 'Shield Defense', 'duration': '15 minutes'},
                    {'name': 'Combat Drills', 'duration': '20 minutes'},
                    {'name': 'Flexibility Training', 'duration': '25 minutes'}
                ],
                'category': 'Combat',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Beginner Hero Training',
                'description': 'Start your hero journey with this beginner-friendly workout',
                'duration': 30,
                'difficulty': 'Beginner',
                'exercises': [
                    {'name': 'Walking', 'duration': '10 minutes'},
                    {'name': 'Light Stretching', 'duration': '10 minutes'},
                    {'name': 'Basic Squats', 'sets': 3, 'reps': 10},
                    {'name': 'Wall Push-ups', 'sets': 3, 'reps': 10}
                ],
                'category': 'General',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'God of Thunder Strength',
                'description': 'Mythical strength training worthy of Asgard',
                'duration': 90,
                'difficulty': 'Expert',
                'exercises': [
                    {'name': 'Hammer Curls', 'sets': 5, 'reps': 12},
                    {'name': 'Deadlifts', 'sets': 5, 'reps': 8},
                    {'name': 'Overhead Press', 'sets': 5, 'reps': 10},
                    {'name': 'Battle Rope', 'duration': '5 minutes'}
                ],
                'category': 'Strength',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Atlantean Swimming',
                'description': 'Master the waters with this comprehensive swimming workout',
                'duration': 60,
                'difficulty': 'Intermediate',
                'exercises': [
                    {'name': 'Freestyle', 'distance': '500m'},
                    {'name': 'Backstroke', 'distance': '300m'},
                    {'name': 'Butterfly', 'distance': '200m'},
                    {'name': 'Underwater Swimming', 'distance': '100m'}
                ],
                'category': 'Swimming',
                'created_at': datetime.utcnow()
            }
        ]
        
        db.workouts.insert_many(workouts)

        # Print summary
        self.stdout.write(self.style.SUCCESS('\nDatabase populated successfully!'))
        self.stdout.write(f'Teams created: {len(teams)}')
        self.stdout.write(f'Users created: {len(users)}')
        self.stdout.write(f'Activities created: {len(activities)}')
        self.stdout.write(f'Leaderboard entries: {len(leaderboard)}')
        self.stdout.write(f'Workout recommendations: {len(workouts)}')

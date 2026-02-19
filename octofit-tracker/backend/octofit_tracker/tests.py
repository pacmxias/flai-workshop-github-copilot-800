from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import datetime
from .models import User, Team, Activity, Leaderboard, Workout


class TeamModelTest(TestCase):
    """Test module for Team model"""

    def setUp(self):
        Team.objects.create(
            name='Test Team',
            description='Test team description'
        )

    def test_team_creation(self):
        team = Team.objects.get(name='Test Team')
        self.assertEqual(team.name, 'Test Team')
        self.assertEqual(team.description, 'Test team description')


class UserModelTest(TestCase):
    """Test module for User model"""

    def setUp(self):
        User.objects.create(
            name='Test User',
            email='test@example.com',
            password='testpass123',
            role='member'
        )

    def test_user_creation(self):
        user = User.objects.get(email='test@example.com')
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'member')


class ActivityModelTest(TestCase):
    """Test module for Activity model"""

    def setUp(self):
        Activity.objects.create(
            user_id='test_user_id',
            user_email='test@example.com',
            user_name='Test User',
            team_id='test_team_id',
            activity_type='running',
            duration=30,
            distance=5.0,
            calories=300,
            date=datetime.now(),
            notes='Morning run'
        )

    def test_activity_creation(self):
        activity = Activity.objects.get(user_email='test@example.com')
        self.assertEqual(activity.activity_type, 'running')
        self.assertEqual(activity.duration, 30)
        self.assertEqual(activity.distance, 5.0)
        self.assertEqual(activity.calories, 300)


class LeaderboardModelTest(TestCase):
    """Test module for Leaderboard model"""

    def setUp(self):
        Leaderboard.objects.create(
            user_id='test_user_id',
            user_email='test@example.com',
            user_name='Test User',
            team_id='test_team_id',
            team_name='Test Team',
            total_calories=1000,
            total_distance=20.0,
            total_duration=100,
            total_activities=5,
            rank=1
        )

    def test_leaderboard_creation(self):
        entry = Leaderboard.objects.get(user_email='test@example.com')
        self.assertEqual(entry.total_calories, 1000)
        self.assertEqual(entry.total_distance, 20.0)
        self.assertEqual(entry.rank, 1)


class WorkoutModelTest(TestCase):
    """Test module for Workout model"""

    def setUp(self):
        Workout.objects.create(
            name='Morning Cardio',
            description='High intensity cardio workout',
            duration=45,
            difficulty='intermediate',
            exercises=['jumping jacks', 'burpees', 'mountain climbers'],
            category='cardio'
        )

    def test_workout_creation(self):
        workout = Workout.objects.get(name='Morning Cardio')
        self.assertEqual(workout.name, 'Morning Cardio')
        self.assertEqual(workout.duration, 45)
        self.assertEqual(workout.difficulty, 'intermediate')


class TeamAPITest(APITestCase):
    """Test module for Team API"""

    def test_create_team(self):
        url = reverse('team-list')
        data = {
            'name': 'API Test Team',
            'description': 'Team created via API'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(Team.objects.get().name, 'API Test Team')


class UserAPITest(APITestCase):
    """Test module for User API"""

    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'name': 'API Test User',
            'email': 'apitest@example.com',
            'password': 'testpass123',
            'role': 'member'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'apitest@example.com')


class ActivityAPITest(APITestCase):
    """Test module for Activity API"""

    def test_create_activity(self):
        url = reverse('activity-list')
        data = {
            'user_id': 'test_user_id',
            'user_email': 'test@example.com',
            'user_name': 'Test User',
            'team_id': 'test_team_id',
            'activity_type': 'running',
            'duration': 30,
            'distance': 5.0,
            'calories': 300,
            'date': datetime.now().isoformat(),
            'notes': 'Test run'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)


class LeaderboardAPITest(APITestCase):
    """Test module for Leaderboard API"""

    def test_create_leaderboard_entry(self):
        url = reverse('leaderboard-list')
        data = {
            'user_id': 'test_user_id',
            'user_email': 'test@example.com',
            'user_name': 'Test User',
            'team_id': 'test_team_id',
            'team_name': 'Test Team',
            'total_calories': 500,
            'total_distance': 10.0,
            'total_duration': 50,
            'total_activities': 3,
            'rank': 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Leaderboard.objects.count(), 1)


class WorkoutAPITest(APITestCase):
    """Test module for Workout API"""

    def test_create_workout(self):
        url = reverse('workout-list')
        data = {
            'name': 'API Test Workout',
            'description': 'Workout created via API',
            'duration': 60,
            'difficulty': 'beginner',
            'exercises': ['push-ups', 'sit-ups'],
            'category': 'strength'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 1)

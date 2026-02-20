from djongo import models


class Team(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class User(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    team_id = models.CharField(max_length=200, null=True, blank=True)
    team_name = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name


class Activity(models.Model):
    _id = models.ObjectIdField()
    user_id = models.CharField(max_length=200)
    user_email = models.EmailField()
    user_name = models.CharField(max_length=200)
    team_id = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    distance = models.FloatField()  # in km
    calories = models.IntegerField()
    date = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'activities'

    def __str__(self):
        return f"{self.user_name} - {self.activity_type}"


class Leaderboard(models.Model):
    _id = models.ObjectIdField()
    user_id = models.CharField(max_length=200)
    user_email = models.EmailField()
    user_name = models.CharField(max_length=200)
    team_id = models.CharField(max_length=200)
    team_name = models.CharField(max_length=200)
    total_calories = models.IntegerField()
    total_distance = models.FloatField()
    total_duration = models.IntegerField()
    total_activities = models.IntegerField()
    rank = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']

    def __str__(self):
        return f"{self.rank}. {self.user_name}"


class Workout(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField()  # in minutes
    difficulty = models.CharField(max_length=50)
    exercises = models.JSONField()
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.name

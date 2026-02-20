#!/usr/bin/env python
import os
import sys
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')

# Setup Django
django.setup()

# Run makemigrations
from django.core.management import call_command

print("Running makemigrations...")
call_command('makemigrations', 'octofit_tracker')
print("Makemigrations completed!")

print("\nRunning migrate...")
call_command('migrate')
print("Migrate completed!")

print("\nPopulating database with test data...")
call_command('populate_db')
print("Database populated successfully!")

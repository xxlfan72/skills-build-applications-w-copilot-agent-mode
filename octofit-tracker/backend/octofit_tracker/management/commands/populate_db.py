from django.core.management.base import BaseCommand
from pymongo import MongoClient

from octofit_tracker import models as app_models


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear collections in dependency-safe order.
        app_models.Activity.objects.all().delete()
        app_models.Leaderboard.objects.all().delete()
        app_models.Workout.objects.all().delete()
        app_models.User.objects.all().delete()
        app_models.Team.objects.all().delete()

        # Create Teams
        marvel = app_models.Team.objects.create(name='team marvel')
        dc = app_models.Team.objects.create(name='team dc')

        # Create Users (super heroes)
        users = [
            app_models.User.objects.create(username='ironman', first_name='Tony', last_name='Stark', email='ironman@marvel.com', password='pass', team=marvel),
            app_models.User.objects.create(username='spiderman', first_name='Peter', last_name='Parker', email='spiderman@marvel.com', password='pass', team=marvel),
            app_models.User.objects.create(username='batman', first_name='Bruce', last_name='Wayne', email='batman@dc.com', password='pass', team=dc),
            app_models.User.objects.create(username='superman', first_name='Clark', last_name='Kent', email='superman@dc.com', password='pass', team=dc),
        ]

        # Create Activities
        [
            app_models.Activity.objects.create(user=users[0], type='run', duration=30, distance=5),
            app_models.Activity.objects.create(user=users[1], type='cycle', duration=45, distance=15),
            app_models.Activity.objects.create(user=users[2], type='swim', duration=60, distance=2),
            app_models.Activity.objects.create(user=users[3], type='run', duration=25, distance=4),
        ]

        # Create Workouts
        [
            app_models.Workout.objects.create(name='Morning Cardio', description='Cardio for all heroes'),
            app_models.Workout.objects.create(name='Strength Training', description='Strength for all heroes'),
        ]

        # Create Leaderboard
        app_models.Leaderboard.objects.create(user=users[0], score=100)
        app_models.Leaderboard.objects.create(user=users[1], score=90)
        app_models.Leaderboard.objects.create(user=users[2], score=95)
        app_models.Leaderboard.objects.create(user=users[3], score=85)

        # Ensure unique index on email
        client = MongoClient('mongodb://localhost:27017')
        client['octofit_db']['users'].create_index('email', unique=True)
        client.close()

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))

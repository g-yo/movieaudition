from django.core.management.base import BaseCommand
from django.utils import timezone
from your_app.models import Movie

class Command(BaseCommand):
    help = 'Deletes movies whose last registration date has passed'

    def handle(self, *args, **kwargs):
        # Get the current date and time
        now = timezone.now()
        
        # Find all movies where last_registration_date is before now
        expired_movies = Movie.objects.filter(last_registration_date__lt=now)
        
        # Count and delete the expired movies
        count, _ = expired_movies.delete()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} expired movie(s).'))

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.timezone import now
from django.conf import settings
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from django import forms
from django.core.validators import FileExtensionValidator


class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    age_start = models.PositiveIntegerField(default=0)
    age_end = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=10)
    number_of_people = models.PositiveIntegerField()
    location_name = models.CharField(max_length=100)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='movie_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Application(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other','Other'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)  # Default to current timestamp
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to='photos/', default='')
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    cv = models.FileField(upload_to='cvs/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True, null=True)  # New field for CV upload
    selected = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} for {self.movie.name}'

@receiver(post_save, sender=Application)
def send_application_notification(sender, instance, created, **kwargs):
    if not created:  # Only send notification on update
        if instance.selected:
            message = f"Congratulations, {instance.name}! You have been selected for {instance.movie.name}."
        else:
            message = f"Sorry, {instance.name}, you have not been selected for {instance.movie.name}."

        # Create a notification for the user
        if instance.user:
            Notification.objects.create(user=instance.user, message=message)


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    
    # Gender choices
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    # Relationships
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def save(self, *args, **kwargs):
        # Calculate age based on date of birth
        if self.date_of_birth:
            today = now().date()
            self.age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        else:
            self.age = None
            
        # Debug print for calculated age
        print(f"Calculated Age: {self.age}")
        
        # Call the original save method
        super().save(*args, **kwargs)

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Changed User to settings.AUTH_USER_MODEL
    feedback_text = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.date_submitted}'

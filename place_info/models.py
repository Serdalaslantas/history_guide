from django.db import models

class LocationQuery(models.Model):
    user_id = models.CharField(max_length=100)
    location_name = models.CharField(max_length=255)
    query_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.location_name}"

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_locations = models.TextField(blank=True, help_text="User's favorite locations, stored as a comma-separated list")

    def __str__(self):
        return self.user.username

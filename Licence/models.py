from django.db import models
from django.contrib.auth.models import User





DAYS_OF_WEEK_CHOICES = (
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday'),
)

class StudyTime(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
from django.db import models
from django.contrib.auth.models import User

class GroupS(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='groups_joined')
    created_at = models.DateTimeField(auto_now_add=True)
    member_count = models.CharField(max_length=10)  # Changed to CharField

    def __str__(self):
        return self.name


class TimeTable(models.Model):
    days = models.CharField(max_length=20)
    period_i = models.CharField(max_length=50)
    period_ii = models.CharField(max_length=50)
    period_iii = models.CharField(max_length=50)
    lunch = models.CharField(max_length=50)
    period_iv = models.CharField(max_length=50)
    period_v = models.CharField(max_length=50)
    period_vi = models.CharField(max_length=50)
    period_vii = models.CharField(max_length=50)

from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username

class Demographics(models.Model):
    user = models.ForeignKey(User)
    age = models.IntegerField(default=0, help_text="Please provide your age (in years).")
    sex = models.CharField(max_length=1, help_text="Please indicate your sex.")
    education_undergrad = models.CharField(max_length=1, default="N")
    education_undergrad_major = models.CharField(max_length=100, default="")
    education_undergrad_year = models.CharField(max_length=1, default="")

    def __unicode__(self):
        return self.user.username

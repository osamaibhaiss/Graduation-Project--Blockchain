from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save
from django.dispatch import receiver
from accounts.models import Profile  # Ensure this line is present

class Voter(models.Model):
    identity_card_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50, blank=True)
    third_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField()
    address = models.TextField()
    has_voted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Login(models.Model):
    voter = models.OneToOneField(Voter, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        if self.pk is None or 'password' in self.changed_data:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

class Election(models.Model):
    election_date = models.DateField()
    election_id= models.AutoField(primary_key=True)
    election_name = models.CharField(max_length=100)
    election_start_time = models.TimeField()
    election_end_time = models.TimeField()
    city = models.CharField(default="", max_length=100)
    seats = models.IntegerField(("Number of Seats"), default=0)

    def __str__(self):
        return self.election_name

class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=100)
    group_description = models.TextField()
    group_image = models.ImageField(upload_to='group_images/', blank=True)
    elections = models.ManyToManyField(Election, related_name='groups')

    def __str__(self):
        return self.group_name


class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='results')
    total_seats = models.IntegerField()
    total_votes = models.IntegerField(default=0)
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='results',
        null=True  # Ensure this is nullable if applicable
    )
class Vote(models.Model):
    voter = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='votes')  # Use Profile for voter
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='votes')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'election')  # Ensure a voter can only vote once in an election

    def __str__(self):
        return f"{self.voter} voted for {self.group} in {self.election}"


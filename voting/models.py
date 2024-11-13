from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save
from django.dispatch import receiver
from accounts.models import Profile  # Ensure this line is present
import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

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
    
    # One-to-one link to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='voter')
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}{self.user.username}"

    @staticmethod
    def generate_random_string(length=8):
        """Generate a random string of a given length."""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
@receiver(post_save, sender=Voter)
def create_user_and_profile(sender, instance, created, **kwargs):
    if created:
        # Generate a random username and password for the new voter
        username = f"voter_{Voter.generate_random_string()}"
        raw_password = Voter.generate_random_string()

        # Create a User for the voter
        user = User.objects.create_user(
            username=username,
            email=f"{username}@example.com",  # Placeholder email
            password=raw_password
        )

        # Store the raw password in the voter instance
        instance.raw_password = raw_password
        instance.save()

        # Create or update the Profile for the voter
        profile, created = Profile.objects.get_or_create(
            user=user,  # Ensure we don't duplicate the profile for the same user
            defaults={
                'phone_number': instance.phone_number,
                'address': instance.address,
                'second_name': instance.second_name,
                'third_name': instance.third_name,
                'identity_card_number': instance.identity_card_number,
                'date_of_birth': instance.date_of_birth
            }
        )

        if created:
            print(f"Profile created for voter {instance.first_name} {instance.last_name} with username: {username}")
        else:
            print(f"Profile already exists for user {username}")
    else:
        # If the Voter is updated, ensure the Profile is updated too
        if hasattr(instance, 'user') and instance.user.profile:
            instance.user.profile.phone_number = instance.phone_number
            instance.user.profile.address = instance.address
            instance.user.profile.second_name = instance.second_name
            instance.user.profile.third_name = instance.third_name
            instance.user.profile.save()


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


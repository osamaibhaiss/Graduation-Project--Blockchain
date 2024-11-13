from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

# accounts/forms.py

from django import forms
from .models import Profile
from voting.models import Voter  # Make sure to import the Voter model

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'second_name', 'third_name', 'identity_card_number', 'date_of_birth']

    # Override the __init__ method to accept voter_instance
    def __init__(self, *args, **kwargs):
        voter_instance = kwargs.pop('voter_instance', None)  # Get the Voter instance from kwargs
        
        super(ProfileForm, self).__init__(*args, **kwargs)  # Call the parent constructor
        
        if voter_instance:
            # Pre-fill the form fields with data from the Voter instance
            self.fields['phone_number'].initial = voter_instance.phone_number
            self.fields['address'].initial = voter_instance.address
            self.fields['second_name'].initial = voter_instance.second_name
            self.fields['third_name'].initial = voter_instance.third_name
            self.fields['identity_card_number'].initial = voter_instance.identity_card_number
            self.fields['date_of_birth'].initial = voter_instance.date_of_birth

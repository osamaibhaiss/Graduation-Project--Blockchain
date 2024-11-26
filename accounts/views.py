# accounts/views.py

from django.shortcuts import render, redirect
from .models import Profile
from .forms import SignupForm, UserForm, ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from voting.models import Voter  # Import the Voter model

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user first
            Profile.objects.create(user=user)  # Create a profile for the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('accounts:profile')  # Redirect to profile view with proper namespace
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def profile_edit(request):
    user_profile = Profile.objects.get(user=request.user)  # Get the user's profile directly
    voter_instance = Voter.objects.filter(user=request.user).first()  # Get associated Voter if exists

    # If Voter instance is available, we will pass it to the ProfileForm
    if request.method == 'POST':
        userform = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=user_profile, voter_instance=voter_instance)  # Pass the Voter instance

        if userform.is_valid() and profile_form.is_valid():
            userform.save()
            profile_form.save()  # Save the profile form directly
            return redirect('/accounts/profile')  # Redirect to the profile page after successful edit

    else:  # Show existing data in forms
        userform = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=user_profile, voter_instance=voter_instance)  # Pass the Voter instance

    return render(request, 'profile_edit.html', {
        'userform': userform,
        'profileform': profile_form,
    })
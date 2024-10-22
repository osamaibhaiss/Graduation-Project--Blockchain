from django.shortcuts import render,redirect
from .models import Profile
from .forms import SignupForm,UserForm,ProfileForm
from django.contrib.auth import authenticate,login
# Create your views here.
from .models import Profile  # Ensure you have this import
from django.contrib.auth.decorators import login_required


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

    if request.method == 'POST':
        userform = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=user_profile)  # Use the renamed variable

        if userform.is_valid() and profile_form.is_valid():
            userform.save()
            profile_form.save()  # Save the profile form directly
            return redirect('/accounts/profile')  # Consider using reverse

    else:  # Show
        userform = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=user_profile)  # Use the renamed variable

    return render(request, 'profile_edit.html', {
        'userform': userform,
        'profileform': profile_form,
    })


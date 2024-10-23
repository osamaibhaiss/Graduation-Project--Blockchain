from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Election, Group, Vote,Result
from django.db import IntegrityError
from accounts.models import Profile
from django.contrib import messages
from django.db.models import Count
from django.db.models import Q

def home1(request):
    return render(request, 'home1.html')

@login_required
def elections(request):
    try:
        user_city = request.user.profile.address  # Get the user's city from their profile
        elections = Election.objects.filter(city=user_city)  # Filter elections by city
        
        # Debugging output
        print(f"Elections for city {user_city}: {elections}")  # Check elections in the console
        
        if not elections:
            messages.warning(request, "No elections found for your city.")
        
        return render(request, 'elections.html', {'elections': elections})

    except AttributeError:
        messages.error(request, "Profile not found. Please complete your profile.")
        return render(request, 'elections.html', {'elections': []})  # Return an empty list if no profile

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Election, Group, Vote

@login_required
def vote(request, election_id):
    voter_profile = getattr(request.user, 'profile', None)
    if not voter_profile:
        messages.error(request, 'Profile not found. Please complete your profile.')
        return redirect('accounts:profile')

    election = get_object_or_404(Election, election_id=election_id)
    groups = election.groups.all()

    # Check if the voter has already voted in this election
    existing_vote = Vote.objects.filter(voter=voter_profile, election=election).first()

    if request.method == 'POST' and not existing_vote:
        group_id = request.POST.get('group')
        group = get_object_or_404(Group, group_id=group_id)

        if group not in election.groups.all():
            messages.error(request, 'Invalid group selection for this election.')
            return redirect('voting:vote', election_id=election.election_id)

        try:
            # Create the vote
            Vote.objects.create(voter=voter_profile, group=group, election=election)

            # Get or create the result for the group
            result, created = Result.objects.get_or_create(group=group, election=election, defaults={'total_votes': 0})
            result.total_votes += 1
            result.save()

            # Mark voter as having voted
            voter_profile.has_voted = True
            voter_profile.save()

            messages.success(request, 'Your vote has been recorded successfully!')
            return redirect('voting:results', election_id=election.election_id)
        except IntegrityError:
            messages.error(request, 'Error occurred while recording your vote. Please try again.')

    return render(request, 'vote.html', {
        'election': election,
        'groups': groups,
        'has_voted': existing_vote is not None  # Pass a flag to the template if the user has already voted
    })

from django.shortcuts import render, get_object_or_404
from .models import Election, Group, Vote  # Ensure you import your models

from django.shortcuts import render, get_object_or_404
from .models import Election, Group, Vote, Profile

def results(request, election_id):
    # Get the election based on the election_id passed in the URL
    election = get_object_or_404(Election, pk=election_id)
    
    # Get all groups participating in the election
    groups = election.groups.all()

    # Initialize a list to store groups and their vote counts
    group_results = []

    # Iterate through the groups and count the votes for each group in this election
    for group in groups:
        total_votes = Vote.objects.filter(group=group, election=election).count()
        group_results.append({
            'group': group,
            'vote_count': total_votes,
        })

    # Get the user's vote if they have voted in this election
    user_vote = None
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        user_vote = Vote.objects.filter(voter=profile, election=election).first()

    context = {
        'election': election,
        'groups': group_results,
        'user_vote': user_vote,
    }

    # Render the results page with the data
    return render(request, 'result.html', context)



@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

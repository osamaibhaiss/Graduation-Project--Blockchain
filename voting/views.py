from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Election, Group, Vote
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
    # Ensure profile exists
    voter_profile = getattr(request.user, 'profile', None)
    if not voter_profile:
        messages.error(request, 'Profile not found. Please complete your profile.')
        return redirect('accounts:profile')

    election = get_object_or_404(Election, election_id=election_id)
    groups = election.groups.all()

    if request.method == 'POST':
        group_id = request.POST.get('group')
        group = get_object_or_404(Group, group_id=group_id)

        if not group in election.groups.all():
            messages.error(request, 'Invalid group selection for this election.')
            return redirect('voting:vote', election_id=election.election_id)

        if not Vote.objects.filter(voter=voter_profile, election=election).exists():
            try:
                # Create the vote
                vote = Vote.objects.create(voter=voter_profile, group=group, election=election)

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
                return redirect('voting:vote', election_id=election.election_id)
        else:
            messages.error(request, 'You have already voted in this election.')
            return redirect('voting:elections')

    return render(request, 'vote.html', {'election': election, 'groups': groups})

from django.shortcuts import render, get_object_or_404
from .models import Election, Group, Vote  # Assuming you have a Vote model

from django.shortcuts import render, get_object_or_404
from .models import Election, Group, Vote  # Ensure you import your models

def results(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    
    # Get groups with their respective results
    groups = election.groups.prefetch_related('results')

    user_vote = None
    if request.user.is_authenticated:
        # Get the user's vote for the current election if applicable
        user_vote = Vote.objects.filter(voter=request.user.profile, election=election).first()

    # Prepare context with group results
    group_results = {}
    for group in groups:
        result = group.results.filter(election=election).first()  # Get result for this group and election
        group_results[group] = result.total_votes if result else 0  # Handle case where result doesn't exist

    context = {
        'election': election,
        'groups': group_results.items(),  # Send the group results as items for rendering
        'user_vote': user_vote,
    }

    return render(request, 'result.html', context)


@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

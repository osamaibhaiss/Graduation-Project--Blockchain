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
        messages.error(request, "Profile not found. Please complete your profile.")
        return redirect('accounts:profile')

    # Load the contract
    web3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))
    contract = web3.eth.contract(address=settings.CONTRACT_ADDRESS, abi=settings.CONTRACT_ABI)

    election = get_object_or_404(Election, pk=election_id)
    groups = election.groups.all()

    existing_vote = Vote.objects.filter(voter=voter_profile, election=election).first()

    if request.method == 'POST' and not existing_vote:
        group_id = request.POST.get('group')
        group = get_object_or_404(Group, pk=group_id)

        try:
            # Send vote to the blockchain
            tx = contract.functions.vote(
                election_id,
                group_id
            ).transact({
                'from': settings.ADMIN_WALLET_ADDRESS,  # Admin wallet
                'gas': 3000000
            })

            # Wait for transaction receipt
            receipt = web3.eth.wait_for_transaction_receipt(tx)
            print(f"Transaction successful: {receipt.transactionHash.hex()}")

            # Save vote in the database
            Vote.objects.create(voter=voter_profile, group=group, election=election)
            messages.success(request, "Your vote has been recorded successfully!")
            return redirect('voting:results', election_id=election_id)

        except Exception as e:
            messages.error(request, f"Error occurred while voting: {e}")

    return render(request, 'vote.html', {
        'election': election,
        'groups': groups,
        'has_voted': existing_vote is not None
    })
from django.shortcuts import render, get_object_or_404
from .models import Election, Group, Vote  # Ensure you import your models

from django.shortcuts import render, get_object_or_404
from .models import Election, Group, Vote, Profile

'''def results(request, election_id):
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
'''


@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

from web3 import Web3
from django.conf import settings
from django.http import JsonResponse
import json

from web3 import Web3
from django.conf import settings
import json

def get_contract():
    ganache_url = 'http://127.0.0.1:7545'  # Ganache local blockchain
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    
    if not web3.is_connected():
        raise Exception("Failed to connect to the blockchain.")

    abi = json.loads(settings.CONTRACT_ABI)
    contract_address = settings.CONTRACT_ADDRESS
    contract = web3.eth.contract(address=contract_address, abi=abi)
    return contract, web3

'''def election_results(request, election_id):
    contract = get_contract()
    
    # Fetch results from the smart contract
    results = contract.functions.getVotes(election_id, 0).call()  # Group ID = 0 as example

    return JsonResponse({
        "vote_count": results
    })'''
def results(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    groups = election.groups.all()

    web3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))
    contract = web3.eth.contract(address=settings.CONTRACT_ADDRESS, abi=settings.CONTRACT_ABI)

    group_results = []
    for group in groups:
        try:
            # Fetch votes from the blockchain
            votes = contract.functions.getVotes(election_id, group.pk).call()
            group_results.append({'group': group, 'vote_count': votes})
        except Exception as e:
            messages.error(request, f"Failed to fetch votes for {group.group_name}: {e}")
            group_results.append({'group': group, 'vote_count': 'Error'})

    return render(request, 'results.html', {
        'election': election,
        'groups': group_results,
    })
    
    

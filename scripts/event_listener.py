import os
from web3 import Web3
import django

# Initialize Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Voting_System.settings')  # Replace with your settings module
django.setup()

from voting.models import Vote, Election, Group  # Import relevant models
from accounts.models import Profile

# Blockchain connection
GANACHE_URL = "http://127.0.0.1:7545"  # Change to your blockchain URL
CONTRACT_ADDRESS = "0xYourSmartContractAddress"
CONTRACT_ABI = [...]  # Replace with your contract ABI

web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def listen_to_vote_cast_events():
    if not web3.is_connected():
        raise Exception("Failed to connect to blockchain.")
    
    print("Connected to blockchain. Listening for events...")
    
    # Create a filter for VoteCast events
    event_filter = contract.events.VoteCast.createFilter(fromBlock='latest')

    while True:
        for event in event_filter.get_new_entries():
            print(f"New VoteCast Event: {event['args']}")

            # Extract data from the event
            voter_address = event['args']['voter']
            election_id = event['args']['electionId']
            group_id = event['args']['groupId']

            # Sync to Django database
            try:
                profile = Profile.objects.get(user__username=voter_address)  # Adjust lookup as needed
                election = Election.objects.get(pk=election_id)
                group = election.groups.get(pk=group_id)

                # Save the vote in the database
                Vote.objects.create(
                    voter=profile,
                    election=election,
                    group=group
                )
                print(f"Vote recorded in database for voter: {profile.user.username}")
            except Exception as e:
                print(f"Failed to sync event to database: {e}")

if __name__ == "__main__":
    listen_to_vote_cast_events()

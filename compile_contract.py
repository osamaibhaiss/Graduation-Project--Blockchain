from solcx import compile_standard, install_solc
import json

# Install the correct Solidity compiler version if not already installed
install_solc('0.8.0')

# The Solidity contract code (replace with the content of your contract)
contract_source_code = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VotingSystem {

    // Define admin wallet address
    address public admin;
    
    // Election struct to store election info
    struct Election {
        string electionName;
        mapping(uint => Group) groups;  // Mapping of groupId to Group
        uint groupCount;
        bool isActive;  // To check if the election is still active
    }
    
    // Group struct to store group name and vote count
    struct Group {
        string groupName;
        uint voteCount;
    }
    
    // Voter struct to store voter info
    struct Voter {
        uint id;
        bool hasVoted;
    }
    
    // Mapping of voters
    mapping(address => Voter) public voters;
    
    // Mapping of elections
    mapping(uint => Election) public elections;
    
    // Mapping of election ID to the current election ID
    uint public currentElectionId;

    // Constructor to set the admin address (should be the wallet that deploys the contract)
    constructor() {
        admin = msg.sender;
    }
    
    // Modifier to allow only admin to execute certain functions
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    // Function to start a new election
    function startElection(string memory electionName) public onlyAdmin {
        currentElectionId++;
        Election storage newElection = elections[currentElectionId];
        newElection.electionName = electionName;
        newElection.isActive = true;
    }

    // Function to add groups to an election
    function addGroupToElection(uint electionId, string memory groupName) public onlyAdmin {
        require(elections[electionId].isActive, "Election is not active");
        Election storage election = elections[electionId];
        election.groups[election.groupCount] = Group(groupName, 0);
        election.groupCount++;
    }

    // Function to register a voter (admin will call this function to register voters)
    function registerVoter(address voterAddress, uint voterId) public onlyAdmin {
        voters[voterAddress] = Voter(voterId, false);
    }

    // Function to vote (only admin can vote for the voters)
    function vote(uint electionId, uint groupId, address voterAddress) public onlyAdmin {
        require(elections[electionId].isActive, "Election is not active");
        require(!voters[voterAddress].hasVoted, "This voter has already voted");
        
        // Mark the voter as having voted
        voters[voterAddress].hasVoted = true;
        
        // Increment the vote count for the group
        Election storage election = elections[electionId];
        require(groupId < election.groupCount, "Invalid groupId");
        election.groups[groupId].voteCount++;
    }

    // Function to get the current vote count for a group
    function getVotes(uint electionId, uint groupId) public view returns (uint) {
        require(elections[electionId].isActive, "Election is not active");
        Election storage election = elections[electionId];
        require(groupId < election.groupCount, "Invalid groupId");
        return election.groups[groupId].voteCount;
    }

    // Function to end an election and stop further voting
    function endElection(uint electionId) public onlyAdmin {
        require(elections[electionId].isActive, "Election is already closed");
        elections[electionId].isActive = false;
    }

    // Function to check if a voter has voted
    function hasVoted(address voterAddress) public view returns (bool) {
        return voters[voterAddress].hasVoted;
    }

    // Function to get the election name
    function getElectionName(uint electionId) public view returns (string memory) {
        return elections[electionId].electionName;
    }
}
"""

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "VotingSystem.sol": {
            "content": contract_source_code
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "evm.bytecode"]
            }
        }
    }
})

# Save ABI and Bytecode
contract_abi = compiled_sol['contracts']['VotingSystem.sol']['VotingSystem']['abi']
contract_bytecode = compiled_sol['contracts']['VotingSystem.sol']['VotingSystem']['evm']['bytecode']['object']

# Save ABI and Bytecode to a file (optional for future use)
with open('VotingSystem_abi.json', 'w') as f:
    json.dump(contract_abi, f)

with open('VotingSystem_bytecode.json', 'w') as f:
    json.dump(contract_bytecode, f)

print("Contract compiled successfully.")

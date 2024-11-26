// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VotingSystem {
    address public admin;

    struct Election {
        string electionName;
        mapping(uint => Group) groups;
        uint groupCount;
        bool isActive;
    }

    struct Group {
        string groupName;
        uint voteCount;
    }

    struct Voter {
        uint id;
        bool hasVoted;
    }

    mapping(address => Voter) public voters;
    mapping(uint => Election) public elections;
    uint public currentElectionId;

    event ElectionStarted(uint electionId, string electionName);
    event ElectionEnded(uint electionId);
    event VoteCast(address indexed voter, uint electionId, uint groupId);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    function startElection(string memory electionName) public onlyAdmin {
        require(bytes(electionName).length > 0, "Election name cannot be empty");

        currentElectionId++;
        Election storage newElection = elections[currentElectionId];
        newElection.electionName = electionName;
        newElection.isActive = true;

        emit ElectionStarted(currentElectionId, electionName);
    }

    function addGroupToElection(uint electionId, string memory groupName) public onlyAdmin {
        require(elections[electionId].isActive, "Election is not active");
        require(bytes(groupName).length > 0, "Group name cannot be empty");

        Election storage election = elections[electionId];
        election.groups[election.groupCount] = Group(groupName, 0);
        election.groupCount++;
    }

    function registerVoter(address voterAddress, uint voterId) public onlyAdmin {
        voters[voterAddress] = Voter(voterId, false);
    }

    function vote(uint electionId, uint groupId) public {
        Voter storage voter = voters[msg.sender];
        require(voter.id != 0, "Voter not registered");
        require(!voter.hasVoted, "Voter has already voted");

        Election storage election = elections[electionId];
        require(election.isActive, "Election is not active");
        require(groupId < election.groupCount, "Invalid groupId");

        voter.hasVoted = true;
        election.groups[groupId].voteCount++;

        emit VoteCast(msg.sender, electionId, groupId);
    }

    function endElection(uint electionId) public onlyAdmin {
        require(elections[electionId].isActive, "Election is already closed");
        elections[electionId].isActive = false;

        emit ElectionEnded(electionId);
    }

    function getVotes(uint electionId, uint groupId) public view returns (uint) {
        Election storage election = elections[electionId];
        require(groupId < election.groupCount, "Invalid groupId");
        return election.groups[groupId].voteCount;
    }

    function hasVoted(address voterAddress) public view returns (bool) {
        return voters[voterAddress].hasVoted;
    }

    function getElectionName(uint electionId) public view returns (string memory) {
        return elections[electionId].electionName;
    }
}


pragma solidity ^0.8.20;

// Insurance claim smart contract using solidity

contract InsuranceClaims {

    // Address of the insurance company
    address public insurer;

    // Store the total number of submitted claims
    uint256 public claimCount;

    // Define the information stored for each claim
    struct Claim {
        uint256 claimId;
        address claimant;
        string policyNumber;
        string description;
        uint256 amount;
        string status;
    }

    // Store claims using their unique ID
    mapping(uint256 => Claim) public claims;

    // Event emitted when a new claim is submitted
    event ClaimSubmitted(
        uint256 claimId,
        address claimant,
        uint256 amount
    );

    // Event triggered when a claim status changes
    event ClaimStatusUpdated(
        uint256 claimId,
        string newStatus
    );

    // Set the insurance company when deploying the contract
    constructor() {
        insurer = msg.sender;
    }

    // Restrict certain functions to the insurance company
    modifier onlyInsurer() {
        require(
            msg.sender == insurer,
            "Only the insurer can perform this action"
        );
        _;
    }

    // Submit a new insurance claim
    function submitClaim(
        string memory _policyNumber,
        string memory _description,
        uint256 _amount
    ) public {

        // Validate the claim information
        require(
            bytes(_policyNumber).length > 0,
            "Policy number is required"
        );

        require(
            bytes(_description).length > 0,
            "Description is required"
        );

        require(
            _amount > 0,
            "Claim amount must be greater than zero"
        );

        // Generate a new claim ID
        claimCount++;

        // Save the claim on the blockchain
        claims[claimCount] = Claim({
            claimId: claimCount,
            claimant: msg.sender,
            policyNumber: _policyNumber,
            description: _description,
            amount: _amount,
            status: "Pending"
        });

        // Record the claim submission event
        emit ClaimSubmitted(
            claimCount,
            msg.sender,
            _amount
        );
    }

    // Approve an insurance claim
    function approveClaim(
        uint256 _claimId
    ) public onlyInsurer {

        // Check whether the claim exists
        require(
            _claimId > 0 && _claimId <= claimCount,
            "Claim does not exist"
        );

        // Check whether the claim is still pending
        require(
            keccak256(bytes(claims[_claimId].status)) ==
            keccak256(bytes("Pending")),
            "Claim has already been processed"
        );

        // Update the claim status
        claims[_claimId].status = "Approved";

        // Record the status change
        emit ClaimStatusUpdated(
            _claimId,
            "Approved"
        );
    }

    // Reject an insurance claim
    function rejectClaim(
        uint256 _claimId
    ) public onlyInsurer {

        // Check whether the claim exists
        require(
            _claimId > 0 && _claimId <= claimCount,
            "Claim does not exist"
        );

        // Check whether the claim is still pending
        require(
            keccak256(bytes(claims[_claimId].status)) ==
            keccak256(bytes("Pending")),
            "Claim has already been processed"
        );

        // Update the claim status
        claims[_claimId].status = "Rejected";

        // Record the status change
        emit ClaimStatusUpdated(
            _claimId,
            "Rejected"
        );
    }

    // Retrieve an insurance claim by its ID
    function getClaim(
        uint256 _claimId
    ) public view returns (
        uint256,
        address,
        string memory,
        string memory,
        uint256,
        string memory
    ) {

        // Check whether the claim exists
        require(
            _claimId > 0 && _claimId <= claimCount,
            "Claim does not exist"
        );

        // Retrieve the stored claim
        Claim memory claim = claims[_claimId];

        return (
            claim.claimId,
            claim.claimant,
            claim.policyNumber,
            claim.description,
            claim.amount,
            claim.status
        );
    }
}

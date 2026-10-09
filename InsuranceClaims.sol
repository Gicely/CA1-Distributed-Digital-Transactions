pragma solidity ^0.8.20;

// Insurance claim smart contract using solidity

contract InsuranceClaims {

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

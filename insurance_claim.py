# Simple Insurance Claim Model - represents the first stage of the blockchain insurance project.
# Fisrt part of the work with python code 

class InsuranceClaim:
    
    def __init__(
        self,
        claim_id,
        customer_name,
        policy_number,
        description,
        claim_amount
    ):
        # Unique identifier for the insurance claim
        self.claim_id = claim_id

        # Name of the customer making the claim
        self.customer_name = customer_name

        # Insurance policy number associated with the customer
        self.policy_number = policy_number

        # Description of the incident or reason for the claim
        self.description = description

        # Amount requested by the customer
        self.claim_amount = claim_amount

        # Every new claim starts with the Pending status
        self.status = "Pending"

    def display_claim(self):

        print("\n--- Insurance Claim ---")
        print(f"Claim ID: {self.claim_id}")
        print(f"Customer: {self.customer_name}")
        print(f"Policy Number: {self.policy_number}")
        print(f"Description: {self.description}")
        print(f"Claim Amount: €{self.claim_amount:.2f}")
        print(f"Status: {self.status}")


# Main program
if __name__ == "__main__":

    # Create a sample insurance claim
    claim = InsuranceClaim(
        claim_id=1,
        customer_name="John Smith",
        policy_number="POL-1001",
        description="Car accident damage",
        claim_amount=2500.00
    )

    # Display the created claim
    claim.display_claim()
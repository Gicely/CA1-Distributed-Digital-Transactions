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
        # This part has information to claim the insurance
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

    # This part is to check if the informations are correct or not
    def validate_claim(self):
       
        if not self.customer_name.strip():
            print("Error: Customer name is required.")
            return False

        if not self.policy_number.strip():
            print("Error: Policy number is required.")
            return False

        if not self.description.strip():
            print("Error: Claim description is required.")
            return False

        # Check that the claim amount is a positive number
        if type(self.claim_amount) not in (int, float):
            print("Error: Claim amount must be a number.")
            return False

        if self.claim_amount <= 0:
            print("Error: Claim amount must be greater than zero.")
            return False

        print("Claim validation successful.")
        return True

    # This parte is to check status and if is valid or not
    def update_status(self, new_status):

        allowed_statuses = ["Approved", "Rejected"]

        # Check whether the new status is valid
        if new_status not in allowed_statuses:
            print("Error: Invalid claim status.")
            return False

        # Prevent changes to claims already processed
        if self.status != "Pending":
            print("Error: Claim has already been processed.")
            return False

        # Validate the claim before changing its status
        if not self.validate_claim():
            print("Error: Cannot process an invalid claim.")
            return False

        # Update the claim status
        self.status = new_status
        print(f"Claim status updated to: {self.status}")
        return True
    
    # This code is to display claim informations
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

    # Validate the claim information
    print("\n--- Claim Validation ---")
    claim.validate_claim()

    # Approve the claim
    print("\n--- Claim Status Update ---")
    claim.update_status("Approved")

    # Display the updated claim
    claim.display_claim()

    # Try to update an already processed claim
    print("\n--- Duplicate Status Update Test ---")
    claim.update_status("Rejected")

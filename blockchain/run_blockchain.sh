# This code is to automate blockchain connection and deployment

# -e stops the programm when has error
set -e

# Move to the project root directory
cd "$(dirname "$0")/.."

echo "========================================"
echo "Insurance Blockchain Application"
echo "========================================"

# Use the Python interpreter from the virtual environment
PYTHON="./.venv/Scripts/python.exe"

# Verify that the virtual environment exists
if [ ! -f "$PYTHON" ]; then
    echo "Error: Python virtual environment not found."
    echo "Create the virtual environment before running this script."
    exit 1
fi

# Verify that the required Python files exist
if [ ! -f "python/blockchain_connection.py" ]; then
    echo "Error: blockchain_connection.py not found."
    exit 1
fi

if [ ! -f "python/contract.py" ]; then
    echo "Error: contract.py not found."
    exit 1
fi

echo ""
echo "Step 1: Connecting to Ganache..."
"$PYTHON" python/blockchain_connection.py

echo ""
echo "Step 2: Deploying the insurance smart contract..."
"$PYTHON" python/contract.py

echo ""
echo "========================================"
echo "Blockchain workflow completed!"
echo "========================================"

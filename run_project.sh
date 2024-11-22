#!/bin/bash

# Define colored output for better readability
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No color

# Step 1: Check if Python and pip are installed
echo -e "${GREEN}Checking Python and pip installation...${NC}"
if ! command -v python &> /dev/null || ! command -v pip &> /dev/null; then
    echo -e "${RED}Python or pip not found. Please install them and try again.${NC}"
    exit 1
fi

# Step 2: Create and activate a virtual environment
echo -e "${GREEN}Setting up a virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python -m venv venv
fi
source venv/bin/activate

# Step 3: Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo -e "${RED}requirements.txt not found. Please ensure it exists in the current directory.${NC}"
    deactivate
    exit 1
fi

# Step 4: Check if config.yaml exists
if [ ! -f "config.yaml" ]; then
    echo -e "${RED}config.yaml not found. Please create a configuration file and try again.${NC}"
    deactivate
    exit 1
fi

# Step 5: Run the Python project
echo -e "${GREEN}Running the Python project...${NC}"
python main.py --config config.yaml

# Step 6: Deactivate the virtual environment
echo -e "${GREEN}Deactivating the virtual environment...${NC}"
deactivate

# to run perform this:   ./run_project.sh

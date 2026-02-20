#!/bin/bash
# Django Setup Fix Script for OctoFit Tracker

set -e  # Exit on error

echo "=== OctoFit Tracker Django Setup Fix ==="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

cd /workspaces/flai-workshop-github-copilot-800

echo -e "${YELLOW}Step 1: Checking virtual environment...${NC}"
if [ ! -d "octofit-tracker/backend/venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv octofit-tracker/backend/venv
else
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
fi

echo ""
echo -e "${YELLOW}Step 2: Activating virtual environment and checking packages...${NC}"
source octofit-tracker/backend/venv/bin/activate

# Check if Django is installed
if ! python -c "import django" 2>/dev/null; then
    echo -e "${YELLOW}Django not found. Installing dependencies...${NC}"
    pip install --upgrade pip
    pip install -r octofit-tracker/backend/requirements.txt
else
    echo -e "${GREEN}✓ Django is installed${NC}"
    django_version=$(python -c "import django; print(django.get_version())")
    echo -e "${GREEN}  Django version: $django_version${NC}"
fi

echo ""
echo -e "${YELLOW}Step 3: Verifying required packages...${NC}"
python -c "
import sys
packages = ['django', 'rest_framework', 'corsheaders', 'djongo', 'pymongo']
missing = []
for pkg in packages:
    try:
        __import__(pkg)
        print(f'✓ {pkg}')
    except ImportError:
        print(f'✗ {pkg} - MISSING')
        missing.append(pkg)
        
if missing:
    print(f'\nError: Missing packages: {missing}')
    sys.exit(1)
"

echo ""
echo -e "${YELLOW}Step 4: Checking MongoDB service...${NC}"
if ps aux | grep -v grep | grep mongod > /dev/null; then
    echo -e "${GREEN}✓ MongoDB is running${NC}"
else
    echo -e "${RED}✗ MongoDB is not running${NC}"
    echo -e "${YELLOW}  Starting MongoDB...${NC}"
    if command -v systemctl &> /dev/null; then
        sudo systemctl start mongodb
    elif command -v service &> /dev/null; then
        sudo service mongodb start
    else
        echo -e "${YELLOW}  Please start MongoDB manually with: sudo mongod --fork --logpath /var/log/mongodb.log${NC}"
    fi
fi

echo ""
echo -e "${YELLOW}Step 5: Testing Django configuration...${NC}"
cd octofit-tracker/backend
python manage.py check --deploy 2>&1 | grep -v "WARNING" || true

echo ""
echo -e "${GREEN}=== Setup Complete ===${NC}"
echo ""
echo "To use Django, activate the virtual environment:"
echo -e "${YELLOW}  source octofit-tracker/backend/venv/bin/activate${NC}"
echo ""
echo "Then run Django commands:"
echo -e "${YELLOW}  cd octofit-tracker/backend${NC}"
echo -e "${YELLOW}  python manage.py runserver 0.0.0.0:8000${NC}"
echo ""

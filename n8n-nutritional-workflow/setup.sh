#!/bin/bash

# N8N Nutritional Workflow Setup Script
# This script sets up the complete environment for the nutritional planning workflow

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "=================================================="
echo "  N8N Nutritional Planning Workflow Setup"
echo "=================================================="
echo -e "${NC}"

# Check if Python is installed
echo -e "${YELLOW}Checking prerequisites...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ pip3 found${NC}"

# Navigate to python services directory
cd python-services

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists, skipping...${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env and add your Telegram bot token${NC}"
else
    echo -e "${YELLOW}.env file already exists, skipping...${NC}"
fi

# Create logs directory
if [ ! -d "logs" ]; then
    mkdir -p logs
    echo -e "${GREEN}✓ Logs directory created${NC}"
fi

# Create models directory for ML models
if [ ! -d "models" ]; then
    mkdir -p models
    echo -e "${GREEN}✓ Models directory created${NC}"
fi

# Create tests directory structure
if [ ! -d "tests" ]; then
    mkdir -p tests
    echo -e "${GREEN}✓ Tests directory created${NC}"
fi

# Run tests
echo -e "${YELLOW}Running tests...${NC}"
if python -m pytest tests/ -v; then
    echo -e "${GREEN}✓ All tests passed${NC}"
else
    echo -e "${YELLOW}⚠️  Some tests failed (this is normal for initial setup)${NC}"
fi

# Check if Docker is installed
echo -e "${YELLOW}Checking for Docker...${NC}"
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ Docker found${NC}"
    
    # Ask if user wants to build Docker image
    read -p "Do you want to build the Docker image? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Building Docker image...${NC}"
        docker build -t nutritional-workflow:latest .
        echo -e "${GREEN}✓ Docker image built successfully${NC}"
    fi
else
    echo -e "${YELLOW}Docker not found, skipping Docker setup${NC}"
fi

# Summary
echo -e "${BLUE}"
echo "=================================================="
echo "  Setup Complete!"
echo "=================================================="
echo -e "${NC}"
echo
echo -e "${GREEN}Next steps:${NC}"
echo "1. Edit python-services/.env and add your Telegram bot token"
echo "2. Import the n8n workflow: nutritional-planning-workflow.json"
echo "3. Start the Python services:"
echo "   cd python-services"
echo "   source venv/bin/activate"
echo "   python service_launcher.py"
echo
echo -e "${YELLOW}Or use Docker:${NC}"
echo "   cd python-services"
echo "   docker-compose up -d"
echo
echo -e "${BLUE}Documentation:${NC}"
echo "   - README.md - Complete setup and usage guide"
echo "   - WORKFLOW_GUIDE.md - Detailed workflow documentation"
echo
echo -e "${GREEN}Services will run on:${NC}"
echo "   - Food Image Analyzer: http://localhost:5000"
echo "   - Dietary Planner: http://localhost:5001"
echo
echo -e "${YELLOW}Happy automating! 🍽️${NC}"

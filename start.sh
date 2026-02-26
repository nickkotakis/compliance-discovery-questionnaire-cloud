#!/bin/bash

# Compliance Discovery Questionnaire - Startup Script
# This script starts both the backend API server and frontend development server

set -e

echo "🚀 Starting Compliance Discovery Questionnaire..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}✗ Node.js is not installed${NC}"
    exit 1
fi

# Backend setup
echo -e "${YELLOW}📦 Setting up backend...${NC}"
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Install package in development mode
echo "Installing compliance_discovery package..."
pip install -q -e .

echo -e "${GREEN}✓ Backend setup complete${NC}"
echo ""

# Start backend server in background
echo -e "${YELLOW}🔧 Starting backend API server on http://localhost:5000${NC}"
python compliance_discovery/api_server.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}✗ Backend failed to start${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Backend server running (PID: $BACKEND_PID)${NC}"
echo ""

# Frontend setup
cd ../frontend

echo -e "${YELLOW}📦 Setting up frontend...${NC}"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
else
    echo "Node modules already installed"
fi

echo -e "${GREEN}✓ Frontend setup complete${NC}"
echo ""

# Start frontend server
echo -e "${YELLOW}🌐 Starting frontend development server on http://localhost:5174${NC}"
echo ""
echo -e "${GREEN}✓ Application is ready!${NC}"
echo ""
echo "Backend API: http://localhost:5000"
echo "Frontend UI: http://localhost:5174"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Start frontend (this will run in foreground)
npm run dev

# Cleanup on exit
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID 2>/dev/null; deactivate; exit" INT TERM

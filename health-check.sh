#!/bin/bash

# Health Check Script for Compliance Discovery Questionnaire
# Verifies that all components are properly configured and can run

set -e

echo "🔍 Compliance Discovery Questionnaire - Health Check"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ERRORS=0

# Check Python
echo -n "Checking Python 3... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3 not found${NC}"
    ((ERRORS++))
fi

# Check Node.js
echo -n "Checking Node.js... "
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Found Node.js $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ Node.js not found${NC}"
    ((ERRORS++))
fi

# Check npm
echo -n "Checking npm... "
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓ Found npm $NPM_VERSION${NC}"
else
    echo -e "${RED}✗ npm not found${NC}"
    ((ERRORS++))
fi

echo ""
echo "Backend Checks:"
echo "---------------"

# Check backend requirements.txt
echo -n "Checking requirements.txt... "
if [ -f "backend/requirements.txt" ]; then
    echo -e "${GREEN}✓ Found${NC}"
else
    echo -e "${RED}✗ Missing${NC}"
    ((ERRORS++))
fi

# Check backend setup.py
echo -n "Checking setup.py... "
if [ -f "backend/setup.py" ]; then
    echo -e "${GREEN}✓ Found${NC}"
else
    echo -e "${RED}✗ Missing${NC}"
    ((ERRORS++))
fi

# Check Python imports
echo -n "Checking Python imports... "
if python3 -c "
import sys
sys.path.insert(0, 'backend')
from compliance_discovery.api_server import app
from compliance_discovery.nist_parser import NIST80053Parser
from compliance_discovery.question_generator import DiscoveryQuestionGenerator
from compliance_discovery.export_generator import ExportGenerator
" 2>/dev/null; then
    echo -e "${GREEN}✓ All imports successful${NC}"
else
    echo -e "${RED}✗ Import errors detected${NC}"
    echo -e "${YELLOW}  Run: cd backend && pip install -r requirements.txt && pip install -e .${NC}"
    ((ERRORS++))
fi

echo ""
echo "Frontend Checks:"
echo "----------------"

# Check package.json
echo -n "Checking package.json... "
if [ -f "frontend/package.json" ]; then
    echo -e "${GREEN}✓ Found${NC}"
else
    echo -e "${RED}✗ Missing${NC}"
    ((ERRORS++))
fi

# Check node_modules
echo -n "Checking node_modules... "
if [ -d "frontend/node_modules" ]; then
    echo -e "${GREEN}✓ Installed${NC}"
else
    echo -e "${YELLOW}⚠ Not installed${NC}"
    echo -e "${YELLOW}  Run: cd frontend && npm install${NC}"
    ((ERRORS++))
fi

# Check TypeScript files
echo -n "Checking TypeScript files... "
if [ -f "frontend/src/App.tsx" ] && [ -f "frontend/src/main.tsx" ]; then
    echo -e "${GREEN}✓ Found${NC}"
else
    echo -e "${RED}✗ Missing core files${NC}"
    ((ERRORS++))
fi

echo ""
echo "Configuration Checks:"
echo "--------------------"

# Check vite.config.ts
echo -n "Checking vite.config.ts... "
if [ -f "frontend/vite.config.ts" ]; then
    echo -e "${GREEN}✓ Found${NC}"
else
    echo -e "${RED}✗ Missing${NC}"
    ((ERRORS++))
fi

# Check tsconfig.json
echo -n "Checking tsconfig.json... "
if [ -f "frontend/tsconfig.json" ]; then
    echo -e "${GREEN}✓ Found${NC}"
else
    echo -e "${RED}✗ Missing${NC}"
    ((ERRORS++))
fi

echo ""
echo "=================================================="

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! System is ready to run.${NC}"
    echo ""
    echo "To start the application, run:"
    echo "  ./start.sh"
    exit 0
else
    echo -e "${RED}✗ Found $ERRORS issue(s). Please fix them before running.${NC}"
    exit 1
fi

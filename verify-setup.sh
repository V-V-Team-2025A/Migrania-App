#!/bin/bash

# CI/CD Setup Verification Script
# Run this script to verify your CI/CD setup is working correctly

echo "🚀 Migraine App CI/CD Setup Verification"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo ""
echo "📋 Checking Prerequisites..."

# Check Python
if command_exists python; then
    PYTHON_VERSION=$(python --version 2>&1)
    echo -e "${GREEN}✅ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python not found${NC}"
fi

# Check Node.js
if command_exists node; then
    NODE_VERSION=$(node --version 2>&1)
    echo -e "${GREEN}✅ Node.js found: $NODE_VERSION${NC}"
else
    echo -e "${RED}❌ Node.js not found${NC}"
fi

# Check Git
if command_exists git; then
    GIT_VERSION=$(git --version 2>&1)
    echo -e "${GREEN}✅ Git found: $GIT_VERSION${NC}"
else
    echo -e "${RED}❌ Git not found${NC}"
fi

echo ""
echo "📁 Checking Project Structure..."

# Check CI/CD files exist
files_to_check=(
    ".github/workflows/ci-cd.yml"
    ".github/workflows/feature-validation.yml"
    ".github/workflows/security-dependencies.yml"
    ".github/CODEOWNERS"
    ".github/BRANCH_PROTECTION.md"
    ".github/IMPLEMENTATION_GUIDE.md"
    "backend/.flake8"
    "backend/pyproject.toml"
    "backend/requirements.txt"
    "frontend/package.json"
    "docker-compose.yaml"
    "Dockerfile"
)

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        print_status 0 "File exists: $file"
    else
        print_status 1 "File missing: $file"
    fi
done

echo ""
echo "🔧 Testing Backend Configuration..."

# Test Django configuration
cd backend 2>/dev/null
if [ $? -eq 0 ]; then
    # Check if manage.py exists
    if [ -f "manage.py" ]; then
        print_status 0 "Django manage.py found"
        
        # Test Django check
        python manage.py check --verbosity=0 2>/dev/null
        print_status $? "Django configuration check"
    else
        print_status 1 "Django manage.py not found"
    fi
    
    # Check if requirements can be read
    if [ -f "requirements.txt" ]; then
        req_count=$(wc -l < requirements.txt)
        print_status 0 "Requirements.txt has $req_count dependencies"
    else
        print_status 1 "Requirements.txt not found"
    fi
    
    cd ..
else
    print_status 1 "Backend directory not accessible"
fi

echo ""
echo "⚛️  Testing Frontend Configuration..."

# Test frontend configuration
cd frontend 2>/dev/null
if [ $? -eq 0 ]; then
    # Check package.json
    if [ -f "package.json" ]; then
        print_status 0 "Frontend package.json found"
        
        # Check if node_modules exists or can install
        if [ -d "node_modules" ]; then
            print_status 0 "Node modules already installed"
        else
            print_warning "Node modules not installed. Run 'npm install' in frontend directory"
        fi
        
        # Test if build script exists
        if npm run build --dry-run 2>/dev/null; then
            print_status 0 "Build script configured"
        else
            print_status 1 "Build script not working"
        fi
        
        # Test if lint script exists
        if npm run lint --dry-run 2>/dev/null; then
            print_status 0 "Lint script configured"
        else
            print_status 1 "Lint script not working"
        fi
    else
        print_status 1 "Frontend package.json not found"
    fi
    
    cd ..
else
    print_status 1 "Frontend directory not accessible"
fi

echo ""
echo "🐳 Testing Docker Configuration..."

# Check Docker files
if [ -f "Dockerfile" ]; then
    print_status 0 "Dockerfile found"
    
    # Basic Dockerfile syntax check
    if grep -q "FROM python" Dockerfile; then
        print_status 0 "Dockerfile uses Python base image"
    else
        print_status 1 "Dockerfile doesn't use Python base image"
    fi
else
    print_status 1 "Dockerfile not found"
fi

if [ -f "docker-compose.yaml" ] || [ -f "docker-compose.yml" ]; then
    print_status 0 "Docker Compose configuration found"
else
    print_status 1 "Docker Compose configuration not found"
fi

echo ""
echo "🔐 Checking Security Configuration..."

# Check if .env files are in .gitignore
if [ -f ".gitignore" ]; then
    if grep -q "\.env" .gitignore; then
        print_status 0 ".env files are gitignored"
    else
        print_warning ".env files should be added to .gitignore"
    fi
else
    print_warning ".gitignore file not found"
fi

echo ""
echo "📊 Summary..."

# Count GitHub workflow files
workflow_count=$(find .github/workflows -name "*.yml" 2>/dev/null | wc -l)
print_status 0 "GitHub workflows configured: $workflow_count"

# Check branch structure
current_branch=$(git branch --show-current 2>/dev/null)
if [[ $current_branch == feature_grupo* ]]; then
    print_status 0 "Currently on feature branch: $current_branch"
elif [[ $current_branch == "dev" ]]; then
    print_status 0 "Currently on dev branch"
elif [[ $current_branch == "main" ]]; then
    print_status 0 "Currently on main branch"
else
    print_warning "Branch name doesn't follow convention: $current_branch"
fi

echo ""
echo "🎯 Next Steps:"
echo "1. ✅ Commit all CI/CD configuration files"
echo "2. ✅ Push your feature branch to GitHub"
echo "3. ✅ Create a Pull Request to 'dev' branch"
echo "4. ✅ Verify GitHub Actions workflows run"
echo "5. ✅ Check automated PR comments"
echo "6. ✅ Ensure deploy team can merge"

echo ""
echo "📚 Documentation:"
echo "- Implementation Guide: .github/IMPLEMENTATION_GUIDE.md"
echo "- Branch Protection Rules: .github/BRANCH_PROTECTION.md"
echo "- CI/CD Overview: .github/README.md"

echo ""
echo "🆘 If you need help:"
echo "- Check the troubleshooting section in IMPLEMENTATION_GUIDE.md"
echo "- Review GitHub Actions logs at: https://github.com/V-V-Team-2025A/Migrania-App/actions"
echo "- Contact your deploy team for permissions issues"

echo ""
echo "✨ Setup verification complete! You're ready to implement CI/CD."

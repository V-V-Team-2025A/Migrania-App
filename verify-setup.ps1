# CI/CD Setup Verification Script for Windows PowerShell
# Run this script to verify your CI/CD setup is working correctly

Write-Host "🚀 Migraine App CI/CD Setup Verification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

function Write-Success {
    param($Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error {
    param($Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Warning {
    param($Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Test-Command {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

Write-Host ""
Write-Host "📋 Checking Prerequisites..." -ForegroundColor Yellow

# Check Python
if (Test-Command "python") {
    $pythonVersion = python --version 2>&1
    Write-Success "Python found: $pythonVersion"
} else {
    Write-Error "Python not found"
}

# Check Node.js
if (Test-Command "node") {
    $nodeVersion = node --version 2>&1
    Write-Success "Node.js found: $nodeVersion"
} else {
    Write-Error "Node.js not found"
}

# Check Git
if (Test-Command "git") {
    $gitVersion = git --version 2>&1
    Write-Success "Git found: $gitVersion"
} else {
    Write-Error "Git not found"
}

Write-Host ""
Write-Host "📁 Checking Project Structure..." -ForegroundColor Yellow

# Check CI/CD files exist
$filesToCheck = @(
    ".github\workflows\ci-cd.yml",
    ".github\workflows\feature-validation.yml", 
    ".github\workflows\security-dependencies.yml",
    ".github\CODEOWNERS",
    ".github\BRANCH_PROTECTION.md",
    ".github\IMPLEMENTATION_GUIDE.md",
    "backend\.flake8",
    "backend\pyproject.toml",
    "backend\requirements.txt",
    "frontend\package.json",
    "docker-compose.yaml",
    "Dockerfile"
)

foreach ($file in $filesToCheck) {
    if (Test-Path $file) {
        Write-Success "File exists: $file"
    } else {
        Write-Error "File missing: $file"
    }
}

Write-Host ""
Write-Host "🔧 Testing Backend Configuration..." -ForegroundColor Yellow

# Test Django configuration
if (Test-Path "backend") {
    Push-Location "backend"
    
    # Check if manage.py exists
    if (Test-Path "manage.py") {
        Write-Success "Django manage.py found"
        
        # Test Django check
        try {
            $checkResult = python manage.py check --verbosity=0 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Django configuration check"
            } else {
                Write-Error "Django configuration has issues"
            }
        }
        catch {
            Write-Error "Django check failed"
        }
    } else {
        Write-Error "Django manage.py not found"
    }
    
    # Check if requirements can be read
    if (Test-Path "requirements.txt") {
        $reqCount = (Get-Content "requirements.txt" | Measure-Object -Line).Lines
        Write-Success "Requirements.txt has $reqCount dependencies"
    } else {
        Write-Error "Requirements.txt not found"
    }
    
    Pop-Location
} else {
    Write-Error "Backend directory not accessible"
}

Write-Host ""
Write-Host "⚛️  Testing Frontend Configuration..." -ForegroundColor Yellow

# Test frontend configuration
if (Test-Path "frontend") {
    Push-Location "frontend"
    
    # Check package.json
    if (Test-Path "package.json") {
        Write-Success "Frontend package.json found"
        
        # Check if node_modules exists
        if (Test-Path "node_modules") {
            Write-Success "Node modules already installed"
        } else {
            Write-Warning "Node modules not installed. Run 'npm install' in frontend directory"
        }
        
        # Test if scripts exist in package.json
        $packageJson = Get-Content "package.json" | ConvertFrom-Json
        if ($packageJson.scripts.build) {
            Write-Success "Build script configured"
        } else {
            Write-Error "Build script not configured"
        }
        
        if ($packageJson.scripts.lint) {
            Write-Success "Lint script configured"
        } else {
            Write-Error "Lint script not configured"
        }
    } else {
        Write-Error "Frontend package.json not found"
    }
    
    Pop-Location
} else {
    Write-Error "Frontend directory not accessible"
}

Write-Host ""
Write-Host "🐳 Testing Docker Configuration..." -ForegroundColor Yellow

# Check Docker files
if (Test-Path "Dockerfile") {
    Write-Success "Dockerfile found"
    
    # Basic Dockerfile syntax check
    $dockerContent = Get-Content "Dockerfile" -Raw
    if ($dockerContent -match "FROM python") {
        Write-Success "Dockerfile uses Python base image"
    } else {
        Write-Error "Dockerfile doesn't use Python base image"
    }
} else {
    Write-Error "Dockerfile not found"
}

if ((Test-Path "docker-compose.yaml") -or (Test-Path "docker-compose.yml")) {
    Write-Success "Docker Compose configuration found"
} else {
    Write-Error "Docker Compose configuration not found"
}

Write-Host ""
Write-Host "🔐 Checking Security Configuration..." -ForegroundColor Yellow

# Check if .env files are in .gitignore
if (Test-Path ".gitignore") {
    $gitignoreContent = Get-Content ".gitignore" -Raw
    if ($gitignoreContent -match "\.env") {
        Write-Success ".env files are gitignored"
    } else {
        Write-Warning ".env files should be added to .gitignore"
    }
} else {
    Write-Warning ".gitignore file not found"
}

Write-Host ""
Write-Host "📊 Summary..." -ForegroundColor Yellow

# Count GitHub workflow files
$workflowCount = 0
if (Test-Path ".github\workflows") {
    $workflowCount = (Get-ChildItem ".github\workflows" -Filter "*.yml").Count
}
Write-Success "GitHub workflows configured: $workflowCount"

# Check branch structure
try {
    $currentBranch = git branch --show-current 2>&1
    if ($currentBranch -match "^feature_grupo\d+") {
        Write-Success "Currently on feature branch: $currentBranch"
    } elseif ($currentBranch -eq "dev") {
        Write-Success "Currently on dev branch"
    } elseif ($currentBranch -eq "main") {
        Write-Success "Currently on main branch"
    } else {
        Write-Warning "Branch name doesn't follow convention: $currentBranch"
    }
}
catch {
    Write-Warning "Could not determine current branch"
}

Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "1. ✅ Commit all CI/CD configuration files"
Write-Host "2. ✅ Push your feature branch to GitHub"
Write-Host "3. ✅ Create a Pull Request to 'dev' branch"
Write-Host "4. ✅ Verify GitHub Actions workflows run"
Write-Host "5. ✅ Check automated PR comments"
Write-Host "6. ✅ Ensure deploy team can merge"

Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "- Implementation Guide: .github\IMPLEMENTATION_GUIDE.md"
Write-Host "- Branch Protection Rules: .github\BRANCH_PROTECTION.md"
Write-Host "- CI/CD Overview: .github\README.md"

Write-Host ""
Write-Host "🆘 If you need help:" -ForegroundColor Cyan
Write-Host "- Check the troubleshooting section in IMPLEMENTATION_GUIDE.md"
Write-Host "- Review GitHub Actions logs at: https://github.com/V-V-Team-2025A/Migrania-App/actions"
Write-Host "- Contact your deploy team for permissions issues"

Write-Host ""
Write-Host "✨ Setup verification complete! You're ready to implement CI/CD." -ForegroundColor Green

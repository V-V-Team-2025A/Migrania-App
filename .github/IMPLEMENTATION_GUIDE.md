# 🚀 CI/CD Implementation Checklist

This checklist will guide you through implementing the CI/CD pipeline step by step.

## ✅ Phase 1: GitHub Configuration (DO THIS FIRST)

### Step 1.1: Verify GitHub Teams ⭐ **CRITICAL**
```bash
# Go to: https://github.com/orgs/V-V-Team-2025A/teams
# Ensure these teams exist:
```

**Required Teams:**
- [ ] `migraine-app-deploy-team` (Can merge to main/dev)
- [ ] `migraine-app-admins` (Repository administrators)
- [ ] `migraine-app-squad1` (Evaluación MIDAS)
- [ ] `migraine-app-squad2` (Bitácora Asistida)
- [ ] `migraine-app-squad3` (Recordatorios)  
- [ ] `migraine-app-squad4` (Estadísticas)
- [ ] `migraine-app-squad5` (Agendamiento)
- [ ] `migraine-app-squad6` (Análisis Patrones)
- [ ] `migraine-app-squad7` (Seguimiento Tratamiento)

### Step 1.2: Configure Branch Protection ⭐ **CRITICAL**
```bash
# Go to: https://github.com/V-V-Team-2025A/Migrania-App/settings/branches
```

**Main Branch (`main`):**
- [ ] ✅ Require pull request reviews (2 reviewers)
- [ ] ✅ Dismiss stale reviews when new commits are pushed
- [ ] ✅ Require review from code owners
- [ ] ✅ Restrict pushes that create files (only `migraine-app-deploy-team`)
- [ ] ✅ Require status checks to pass:
  - [ ] `lint-and-format`
  - [ ] `backend-tests`
  - [ ] `frontend-tests`
  - [ ] `security-scan`
  - [ ] `build-and-push`
- [ ] ✅ Require branches to be up to date before merging
- [ ] ❌ Allow force pushes: **NO**
- [ ] ❌ Allow deletions: **NO**

**Dev Branch (`dev`):**
- [ ] ✅ Require pull request reviews (1 reviewer)
- [ ] ✅ Dismiss stale reviews when new commits are pushed
- [ ] ✅ Restrict pushes that create files (only `migraine-app-deploy-team`)
- [ ] ✅ Require status checks to pass:
  - [ ] `lint-and-format`
  - [ ] `backend-tests`
  - [ ] `frontend-tests`
- [ ] ✅ Require branches to be up to date before merging
- [ ] ❌ Allow force pushes: **NO**
- [ ] ❌ Allow deletions: **NO**

**Feature Branches (`feature/*`):**
- [ ] ✅ Require pull request reviews (1 reviewer from same squad)
- [ ] ✅ Require status checks to pass:
  - [ ] `feature-quality-check`
  - [ ] `feature-tests`
- [ ] ✅ Auto-delete head branches after merge

### Step 1.3: Set Up Environments ⭐ **CRITICAL**
```bash
# Go to: https://github.com/V-V-Team-2025A/Migrania-App/settings/environments
```

**Development Environment:**
- [ ] Name: `development`
- [ ] Protection rules: None (auto-deploy)
- [ ] Required reviewers: None

**Staging Environment:**
- [ ] Name: `staging`
- [ ] Protection rules: Required reviewers
- [ ] Required reviewers: 1 from `migraine-app-deploy-team`
- [ ] Wait timer: 0 minutes

**Production Environment:**
- [ ] Name: `production`
- [ ] Protection rules: Required reviewers
- [ ] Required reviewers: 2 from `migraine-app-deploy-team`
- [ ] Wait timer: 5 minutes
- [ ] Deployment branches: Only `main`

## ✅ Phase 2: Secrets Configuration

### Step 2.1: Repository Secrets ⭐ **CRITICAL**
```bash
# Go to: https://github.com/V-V-Team-2025A/Migrania-App/settings/secrets/actions
```

**Generate SSH Keys for Deployments:**
```powershell
# Run these commands in PowerShell to generate keys:
ssh-keygen -t ed25519 -C "migraine-app-dev" -f $HOME\.ssh\migraine_dev
ssh-keygen -t ed25519 -C "migraine-app-staging" -f $HOME\.ssh\migraine_staging
ssh-keygen -t ed25519 -C "migraine-app-prod" -f $HOME\.ssh\migraine_prod
```

**Add these secrets:**
- [ ] `DEPLOY_KEY_DEV`: Content of `migraine_dev` (private key)
- [ ] `DEPLOY_KEY_STAGING`: Content of `migraine_staging` (private key)
- [ ] `DEPLOY_KEY_PROD`: Content of `migraine_prod` (private key)
- [ ] `DATABASE_URL_PROD`: `postgresql://user:password@prod-server:5432/migraine_db`
- [ ] `SECRET_KEY_PROD`: Django production secret key (generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- [ ] `SLACK_WEBHOOK_URL`: (Optional) Your Slack webhook for notifications

### Step 2.2: Environment Variables
**Production Environment Variables:**
- [ ] `DEBUG`: `false`
- [ ] `ALLOWED_HOSTS`: `your-production-domain.com,api.your-domain.com`
- [ ] `CORS_ALLOWED_ORIGINS`: `https://your-frontend-domain.com`

**Staging Environment Variables:**
- [ ] `DEBUG`: `true`
- [ ] `ALLOWED_HOSTS`: `staging.your-domain.com,api-staging.your-domain.com`
- [ ] `CORS_ALLOWED_ORIGINS`: `https://staging.your-domain.com`

## ✅ Phase 3: Code Quality Setup

### Step 3.1: Backend Configuration ✅ **DONE**
- [x] ✅ Created `.flake8` configuration
- [x] ✅ Updated `pyproject.toml` with black, isort, flake8 settings
- [x] ✅ Django project passes basic checks

### Step 3.2: Frontend Configuration
- [x] ✅ Fixed `vite.config.js` linting issues
- [ ] **Fix remaining linting issues:**

**Fix unused variables in Bitacora components:**
```javascript
// In: frontend/src/features/feature_Grupo2_BitacoraAsistidaCefalea/pages/Bitacora-Medico.jsx
// In: frontend/src/features/feature_Grupo2_BitacoraAsistidaCefalea/pages/Bitacora-Paciente.jsx
// Either use 'setEpisodios' or prefix with '_' to ignore: const [episodios, _setEpisodios] = useState([]);
```

### Step 3.3: Install Code Quality Tools Locally
```powershell
# Backend
cd backend
pip install black isort flake8 safety

# Frontend is already configured with ESLint
```

## ✅ Phase 4: Test Workflow Locally

### Step 4.1: Backend Local Testing
```powershell
cd backend

# Test Django
python manage.py check
python manage.py collectstatic --noinput --dry-run

# Test code quality
black --check .
isort --check-only .
flake8 .

# Test BDD (if you have features)
behave --dry-run
```

### Step 4.2: Frontend Local Testing
```powershell
cd frontend

# Test build and lint
npm run lint
npm run build
```

## ✅ Phase 5: Commit and Deploy

### Step 5.1: Fix Code Quality Issues
- [ ] Fix all linting errors found in frontend
- [ ] Ensure all backend code passes quality checks
- [ ] Test that Django migrations work

### Step 5.2: Commit CI/CD Configuration
```bash
git add .github/
git add backend/.flake8
git add backend/pyproject.toml
git add frontend/vite.config.js
git commit -m "feat: Add CI/CD pipeline configuration

- Add GitHub Actions workflows for CI/CD
- Add feature validation pipeline
- Add security and dependency management  
- Configure code quality tools
- Update CODEOWNERS for deploy team structure"
```

### Step 5.3: Create Pull Request to Dev
```bash
# Push your feature branch
git push origin feature_grupo7_generacion_seguimiento_tratamiento

# Create PR to dev branch via GitHub UI
# The feature validation workflow will run automatically
```

## ✅ Phase 6: Workflow Testing

### Step 6.1: Test Feature Validation
- [ ] Create a PR from your feature branch to `dev`
- [ ] Verify that `Feature Branch Validation` workflow runs
- [ ] Check that automated PR comment appears
- [ ] Ensure all checks pass

### Step 6.2: Test Main CI/CD Pipeline
- [ ] After deploy team merges your PR to `dev`
- [ ] Verify that full CI/CD pipeline runs
- [ ] Check that Docker image builds successfully
- [ ] Verify deployment to development environment

### Step 6.3: Test Production Pipeline
- [ ] After deploy team merges `dev` to `main`
- [ ] Verify production deployment workflow
- [ ] Check security scanning results
- [ ] Verify all environments are updated

## ✅ Phase 7: Team Onboarding

### Step 7.1: Squad Training
**For Each Squad (1-7):**
- [ ] Explain branching strategy: `feature_grupo[N]_description`
- [ ] Show how to run local code quality checks
- [ ] Demonstrate PR process and automated feedback
- [ ] Explain deployment approval process

### Step 7.2: Deploy Team Training
**For Deploy Team:**
- [ ] Show GitHub Actions interface
- [ ] Explain environment protection rules
- [ ] Demonstrate manual deployment approvals
- [ ] Show monitoring and notification setup

## ✅ Phase 8: Production Checklist

### Step 8.1: Before Going Live
- [ ] All secrets configured correctly
- [ ] Production environment variables set
- [ ] Database connections tested
- [ ] SSL certificates configured
- [ ] Domain names pointed correctly
- [ ] Backup procedures in place

### Step 8.2: Monitoring Setup
- [ ] Set up application monitoring (optional)
- [ ] Configure log aggregation (optional)
- [ ] Set up alert notifications
- [ ] Create incident response procedures

## 🚨 Troubleshooting

### Common Issues

**Workflow Fails:**
```bash
# Check workflow logs in GitHub Actions tab
# View specific job details
# Check secrets are configured correctly
```

**Permission Denied:**
```bash
# Verify team memberships
# Check branch protection rules
# Ensure proper CODEOWNERS configuration
```

**Tests Fail:**
```bash
# Run tests locally first
# Check database configuration  
# Verify dependencies are installed
```

## 📞 Support

| Issue Type | Contact | Action |
|------------|---------|---------|
| GitHub Teams Setup | Repository Admin | Create GitHub issue |
| Branch Protection | `migraine-app-deploy-team` | Slack/Teams message |
| CI/CD Pipeline | `migraine-app-deploy-team` | GitHub Discussions |
| Code Quality | Squad Lead | Squad channel |
| Security Issues | `migraine-app-admins` | Direct message |

---

## 🎯 Success Criteria

✅ **You'll know it's working when:**
1. Feature branches trigger validation workflows
2. PRs get automated feedback comments
3. Dev merges trigger full CI/CD pipeline
4. Docker images build and push successfully
5. Deployments require proper approvals
6. Security scans run daily
7. Dependencies update automatically
8. All team members can contribute following the workflow

---

**Next Steps After Setup:**
1. Train all squad members on the workflow
2. Set up monitoring and alerting
3. Configure actual deployment scripts
4. Implement additional security measures
5. Add performance testing to the pipeline

Good luck with your implementation! 🚀

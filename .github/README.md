# CI/CD Pipeline for Migraine App

This repository contains a comprehensive CI/CD pipeline designed for a multi-squad development environment following the Spotify model. The pipeline supports 7 feature squads working on different aspects of the migraine tracking application.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     CI/CD Pipeline Architecture                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Feature Branches (Squad 1-7)                                  │
│  │                                                             │
│  ├── feature_grupo1_evaluacion_midas                          │
│  ├── feature_grupo2_bitacora_asistida                         │
│  ├── feature_grupo3_recordatorios                             │
│  ├── feature_grupo4_estadisticas_historial                    │
│  ├── feature_grupo5_agendamiento_citas                        │
│  ├── feature_grupo6_analisis_patrones                         │
│  └── feature_grupo7_generacion_seguimiento_tratamiento        │
│       │                                                        │
│       └── Feature Validation Pipeline                          │
│           ├── PR Validation                                    │
│           ├── Code Quality Check                               │
│           ├── Feature-specific Tests                           │
│           └── Automated PR Comments                            │
│                                                                │
│  Dev Branch (Integration)                                      │
│  │                                                             │
│  └── Full CI/CD Pipeline                                       │
│      ├── Lint & Format                                         │
│      ├── Backend Tests (Django + BDD)                          │
│      ├── Frontend Tests                                        │
│      ├── Security Scanning                                     │
│      ├── Docker Build & Push                                   │
│      ├── Deploy to Development                                 │
│      ├── Deploy to Staging                                     │
│      └── Integration Tests                                     │
│                                                                │
│  Main Branch (Production)                                      │
│  │                                                             │
│  └── Production Pipeline                                       │
│      ├── All CI Checks                                         │
│      ├── Security Validation                                   │
│      ├── Production Deployment                                 │
│      └── Post-deployment Verification                          │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Workflows

### 1. Main CI/CD Pipeline (`ci-cd.yml`)

**Triggers**: Push to `main`, `dev`, `feature/*` branches and PRs

**Jobs**:
- **Lint and Format**: Code quality checks for both backend (Python) and frontend (JavaScript)
- **Backend Tests**: Django unit tests and BDD tests with Behave
- **Frontend Tests**: Build validation and linting
- **Security Scan**: Trivy vulnerability scanning
- **Build and Push**: Docker image creation and registry push
- **Deploy to Development**: Automatic deployment for `dev` branch
- **Deploy to Staging**: Staging environment deployment
- **Deploy to Production**: Production deployment for `main` branch
- **Integration Tests**: E2E testing post-deployment
- **Notification**: Team notifications

### 2. Feature Validation (`feature-validation.yml`)

**Triggers**: Pull requests to `dev` and `main` branches

**Jobs**:
- **PR Validation**: Branch naming and PR title format validation
- **Feature Quality Check**: Squad-specific code quality validation
- **Feature Tests**: Targeted testing for specific squad features
- **PR Comments**: Automated feedback on pull requests

### 3. Security and Dependencies (`security-dependencies.yml`)

**Triggers**: Daily schedule, dependency file changes, manual trigger

**Jobs**:
- **Dependency Scan**: Vulnerability scanning for Python and Node.js dependencies
- **License Check**: License compliance validation
- **Automated Updates**: Daily dependency update PRs
- **Security Advisory**: GitHub security advisory monitoring
- **Compliance Report**: Security and compliance reporting

## 🏆 Squad Structure

| Squad | Focus Area | Backend App | Branch Pattern |
|-------|------------|-------------|----------------|
| Squad 1 | Evaluación MIDAS | `evaluacion_diagnostico` | `feature_grupo1_*` |
| Squad 2 | Bitácora Asistida | `evaluacion_diagnostico` | `feature_grupo2_*` |
| Squad 3 | Recordatorios | `tratamiento` | `feature_grupo3_*` |
| Squad 4 | Estadísticas | `analiticas` | `feature_grupo4_*` |
| Squad 5 | Agendamiento | `agendamiento_citas` | `feature_grupo5_*` |
| Squad 6 | Análisis Patrones | `analiticas` | `feature_grupo6_*` |
| Squad 7 | Seguimiento Tratamiento | `tratamiento` | `feature_grupo7_*` |

## 🔧 Technology Stack

### Backend
- **Framework**: Django 5.2.4
- **Database**: PostgreSQL
- **Testing**: Django TestCase + Behave (BDD)
- **Package Management**: UV
- **API**: Django REST Framework

### Frontend
- **Framework**: React 19.1.0
- **Build Tool**: Vite 7.0.3
- **Linting**: ESLint
- **Routing**: React Router DOM

### Infrastructure
- **Containerization**: Docker
- **Registry**: GitHub Container Registry (ghcr.io)
- **CI/CD**: GitHub Actions
- **Security**: Trivy, Safety, NPM Audit

## 📋 Prerequisites

### Repository Setup
1. **GitHub Teams**: Create teams for each squad (`migraine-app-squad1` through `migraine-app-squad7`)
2. **Branch Protection**: Configure protection rules for `main` and `dev` branches
3. **Environments**: Set up `development`, `staging`, and `production` environments
4. **Secrets**: Configure required secrets (see below)

### Required Secrets
```yaml
# GitHub Repository Secrets
GITHUB_TOKEN: # Automatically provided by GitHub
DEPLOY_KEY_DEV: # SSH key for development deployment
DEPLOY_KEY_STAGING: # SSH key for staging deployment  
DEPLOY_KEY_PROD: # SSH key for production deployment
SLACK_WEBHOOK_URL: # Optional: for notifications
DATABASE_URL_PROD: # Production database connection string
SECRET_KEY_PROD: # Production Django secret key
```

### Environment Variables
```yaml
# Environment-specific variables
DEBUG: false # for production
ALLOWED_HOSTS: "your-domain.com,api.your-domain.com"
CORS_ALLOWED_ORIGINS: "https://your-frontend-domain.com"
```

## 🚦 Pipeline Flow

### Feature Development Flow
1. **Developer** creates feature branch: `feature_grupo[1-7]_description`
2. **Feature Validation** runs automatically on PR creation
3. **Code Quality** checks ensure standards compliance
4. **Squad-specific Tests** validate feature functionality
5. **Automated PR Comments** provide feedback
6. **Squad Review** required before merge to `dev`

### Integration Flow (Dev Branch)
1. **Full CI Pipeline** runs on merge to `dev`
2. **Security Scanning** validates dependencies
3. **Docker Build** creates deployment artifact
4. **Auto-deploy** to development environment
5. **Manual Approval** required for staging deployment
6. **Integration Tests** run against staging

### Production Flow (Main Branch)
1. **Enhanced Security** checks on production code
2. **Production Build** with optimizations
3. **Manual Approval** required for production deployment
4. **Blue-Green Deployment** for zero-downtime updates
5. **Post-deployment Verification** ensures system health

## 🧪 Testing Strategy

### Backend Testing
- **Unit Tests**: Django TestCase for models, views, services
- **BDD Tests**: Behave with Gherkin features for user stories
- **Integration Tests**: API endpoint testing
- **Database Tests**: Migration and data integrity tests

### Frontend Testing
- **Build Tests**: Vite build validation
- **Lint Tests**: ESLint code quality
- **Component Tests**: React component testing (to be added)
- **E2E Tests**: Playwright/Cypress integration (to be added)

### Test Coverage
- **Minimum Coverage**: 80% for new code
- **Coverage Reports**: Uploaded to Codecov
- **Coverage Gates**: PR merge blocked if coverage drops

## 🔒 Security Features

### Automated Security Scanning
- **Dependency Vulnerabilities**: Daily scans with Safety and NPM Audit
- **Container Scanning**: Trivy scans for Docker images
- **License Compliance**: Automated license checking
- **Security Advisories**: GitHub advisory monitoring

### Security Policies
- **Dependency Updates**: Automated daily updates
- **Vulnerability Response**: Automatic issue creation for critical CVEs
- **Security Reviews**: Required for production deployments
- **Secret Management**: GitHub Secrets for sensitive data

## 📊 Monitoring and Reporting

### Pipeline Metrics
- **Build Success Rate**: Track pipeline reliability
- **Test Coverage**: Monitor code coverage trends
- **Deployment Frequency**: Measure delivery velocity
- **Mean Time to Recovery**: Track incident response

### Reports Generated
- **Security Reports**: Daily vulnerability assessments
- **Compliance Reports**: License and policy compliance
- **Test Reports**: JUnit XML format for integration
- **Coverage Reports**: XML format for external tools

## 🔄 Branch Protection Rules

### Main Branch
- ✅ Require PR reviews (2 reviewers)
- ✅ Require status checks
- ✅ Require up-to-date branches
- ✅ Include administrators in restrictions
- ❌ Allow force pushes
- ❌ Allow deletions

### Dev Branch
- ✅ Require PR reviews (1 reviewer)
- ✅ Require status checks
- ✅ Require up-to-date branches
- ❌ Allow force pushes
- ❌ Allow deletions

### Feature Branches
- ✅ Auto-delete after merge
- ✅ Squad-specific review requirements

## 🚨 Troubleshooting

### Common Issues

#### Pipeline Failures
```bash
# Check workflow logs
gh run list --repo V-V-Team-2025A/Migrania-App

# View specific run details
gh run view <run-id> --repo V-V-Team-2025A/Migrania-App
```

#### Test Failures
```bash
# Run tests locally (Backend)
cd backend
python manage.py test --verbosity=2

# Run BDD tests locally
behave features/ --junit --junit-directory=test-reports

# Run frontend tests locally
cd frontend
npm run lint
npm run build
```

#### Security Issues
```bash
# Check for vulnerabilities (Backend)
cd backend
safety check

# Check for vulnerabilities (Frontend)
cd frontend
npm audit
```

### Getting Help

| Issue Type | Contact | Method |
|------------|---------|---------|
| CI/CD Pipeline | `@migraine-app-admins` | GitHub Issues |
| Feature Development | Squad Lead | Slack/Teams |
| Security Concerns | `@migraine-app-admins` | Direct Message |
| Infrastructure | DevOps Team | GitHub Discussions |

## 📈 Metrics and KPIs

### Development Metrics
- **Deployment Frequency**: Target 2-3 deployments per week
- **Lead Time**: Feature development to production < 2 weeks
- **Change Failure Rate**: < 5% of deployments cause incidents
- **Mean Time to Recovery**: < 2 hours for critical issues

### Quality Metrics
- **Test Coverage**: Maintain > 80% coverage
- **Code Quality**: Zero critical security vulnerabilities
- **Build Success Rate**: > 95% pipeline success rate
- **Review Time**: Average PR review time < 24 hours

## 🎯 Future Enhancements

### Planned Improvements
- [ ] **Performance Testing**: Automated load testing integration
- [ ] **Visual Regression**: Screenshot comparison testing
- [ ] **Chaos Engineering**: Automated resilience testing
- [ ] **Advanced Monitoring**: APM integration (Datadog/New Relic)
- [ ] **Mobile CI/CD**: React Native pipeline (if mobile app planned)

### Integration Roadmap
- [ ] **Kubernetes Deployment**: Migrate from Docker Compose
- [ ] **GitOps Workflow**: ArgoCD integration
- [ ] **Multi-environment**: Additional staging environments
- [ ] **A/B Testing**: Feature flag integration

---

## 📝 Contributing

1. **Create Feature Branch**: Follow naming convention `feature_grupo[1-7]_description`
2. **Develop Feature**: Follow coding standards and write tests
3. **Create Pull Request**: Use conventional commit messages
4. **Review Process**: Ensure squad member review
5. **Merge Requirements**: All checks must pass

For detailed contribution guidelines, see [CONTRIBUTING.md](./CONTRIBUTING.md)

---

*This CI/CD pipeline is maintained by the Migraine App development team. For questions or support, please contact the repository administrators.*

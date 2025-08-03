# Branch Protection Rules Configuration

This document outlines the recommended branch protection rules for the Migraine App repository following the Spotify model with GitHub Teams.

## Repository Structure

```
main (production)
├── dev (staging/integration)
│   ├── feature_grupo1_evaluacion_midas
│   ├── feature_grupo2_bitacora_asistida
│   ├── feature_grupo3_recordatorios
│   ├── feature_grupo4_estadisticas_historial
│   ├── feature_grupo5_agendamiento_citas
│   ├── feature_grupo6_analisis_patrones
│   └── feature_grupo7_generacion_seguimiento_tratamiento
```

## Branch Protection Rules

### Main Branch (Production)
- **Require pull request reviews**: Yes (2 reviewers minimum)
- **Dismiss stale reviews**: Yes
- **Require review from code owners**: Yes
- **Require status checks**: Yes
  - `lint-and-format`
  - `backend-tests`
  - `frontend-tests`
  - `security-scan`
  - `build-and-push`
- **Require branches to be up to date**: Yes
- **Require signed commits**: Recommended
- **Include administrators**: No (allows emergency fixes)
- **Allow force pushes**: No
- **Allow deletions**: No

### Dev Branch (Staging)
- **Require pull request reviews**: Yes (1 reviewer minimum)
- **Dismiss stale reviews**: Yes
- **Require status checks**: Yes
  - `lint-and-format`
  - `backend-tests`
  - `frontend-tests`
- **Require branches to be up to date**: Yes
- **Include administrators**: No
- **Allow force pushes**: No
- **Allow deletions**: No

### Feature Branches
- **Require pull request reviews**: Yes (1 reviewer from same squad)
- **Require status checks**: Yes
  - `feature-quality-check`
  - `feature-tests`
- **Auto-delete after merge**: Yes

## GitHub Teams Setup

### Recommended Teams Structure

1. **migraine-app-admins**
   - Repository administrators
   - Can merge to main
   - Full repository access

2. **migraine-app-leads**
   - Tech leads and architects
   - Can review and approve PRs to main
   - Can merge to dev

3. **migraine-app-squad1** (Evaluación MIDAS)
   - Members working on `feature_grupo1_*` branches
   - Can create and merge feature PRs

4. **migraine-app-squad2** (Bitácora Asistida)
   - Members working on `feature_grupo2_*` branches

5. **migraine-app-squad3** (Recordatorios)
   - Members working on `feature_grupo3_*` branches

6. **migraine-app-squad4** (Estadísticas)
   - Members working on `feature_grupo4_*` branches

7. **migraine-app-squad5** (Agendamiento)
   - Members working on `feature_grupo5_*` branches

8. **migraine-app-squad6** (Análisis Patrones)
   - Members working on `feature_grupo6_*` branches

9. **migraine-app-squad7** (Seguimiento Tratamiento)
   - Members working on `feature_grupo7_*` branches

## CODEOWNERS File

Create a `.github/CODEOWNERS` file:

```
# Global owners
* @migraine-app-admins @migraine-app-leads

# Backend applications
/backend/evaluacion_diagnostico/ @migraine-app-squad1 @migraine-app-squad2
/backend/tratamiento/ @migraine-app-squad3 @migraine-app-squad7
/backend/analiticas/ @migraine-app-squad4 @migraine-app-squad6
/backend/agendamiento_citas/ @migraine-app-squad5
/backend/usuarios/ @migraine-app-leads

# Frontend features
/frontend/src/features/feature_Grupo1_*/ @migraine-app-squad1
/frontend/src/features/feature_Grupo2_*/ @migraine-app-squad2
/frontend/src/features/feature_Grupo3_*/ @migraine-app-squad3
/frontend/src/features/feature_Grupo4_*/ @migraine-app-squad4
/frontend/src/features/feature_Grupo5_*/ @migraine-app-squad5
/frontend/src/features/feature_Grupo6_*/ @migraine-app-squad6
/frontend/src/features/feature_Grupo7_*/ @migraine-app-squad7

# Infrastructure and CI/CD
/.github/ @migraine-app-admins
/docker-compose.yaml @migraine-app-admins
/Dockerfile @migraine-app-admins
```

## Environment Protection Rules

### Production Environment
- **Required reviewers**: 2 from `migraine-app-admins`
- **Wait timer**: 5 minutes
- **Deployment branches**: Only `main`

### Staging Environment
- **Required reviewers**: 1 from `migraine-app-leads`
- **Deployment branches**: Only `dev`

### Development Environment
- **Required reviewers**: None (auto-deploy)
- **Deployment branches**: `dev` and `feature/*`

## Workflow Permissions

### Repository Secrets Required
- `GITHUB_TOKEN`: Automatically provided
- `DEPLOY_KEY_DEV`: SSH key for development deployment
- `DEPLOY_KEY_STAGING`: SSH key for staging deployment
- `DEPLOY_KEY_PROD`: SSH key for production deployment
- `SLACK_WEBHOOK_URL`: For notifications (optional)
- `DATABASE_URL_PROD`: Production database connection
- `SECRET_KEY_PROD`: Production Django secret key

### Environment Variables
- `DEBUG`: Set to `false` for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `CORS_ALLOWED_ORIGINS`: Allowed frontend origins

## Setup Instructions

1. **Create GitHub Teams**:
   ```bash
   # Use GitHub CLI or web interface to create teams
   gh api orgs/V-V-Team-2025A/teams -f name="migraine-app-squad1" -f description="Squad 1 - Evaluación MIDAS"
   ```

2. **Configure Branch Protection**:
   - Go to Settings > Branches
   - Add rules for `main`, `dev`, and `feature/*` patterns

3. **Set Up Environments**:
   - Go to Settings > Environments
   - Create `development`, `staging`, and `production` environments

4. **Add Secrets**:
   - Go to Settings > Secrets and variables > Actions
   - Add required secrets and environment variables

5. **Create CODEOWNERS**:
   ```bash
   # Create the file in .github/CODEOWNERS
   ```

6. **Test Workflows**:
   - Create a test feature branch
   - Open a PR to verify all checks run correctly

## Best Practices

1. **Feature Branch Naming**: Always use `feature_grupo[1-7]_description` format
2. **Commit Messages**: Use conventional commit format
3. **PR Reviews**: Require reviews from relevant squad members
4. **Testing**: Ensure all tests pass before merging
5. **Documentation**: Update documentation with feature changes
6. **Security**: Regular dependency updates and security scans

## Troubleshooting

### Common Issues

1. **Tests Failing**: Check test output in Actions tab
2. **Branch Protection**: Ensure status checks are configured correctly
3. **Permissions**: Verify team memberships and repository access
4. **Secrets**: Ensure all required secrets are configured

### Support Contacts

- **CI/CD Issues**: `@migraine-app-admins`
- **Feature Questions**: Contact relevant squad lead
- **Security Concerns**: `@migraine-app-admins`

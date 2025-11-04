# CI/CD Pipeline

The CI/CD pipeline will manage automated testing, security scanning, container building, and deployment promotions for PhishGuard.

## Planned Stages

1. **Lint & Test**: Run unit tests, type checks (mypy), and linting (ruff, eslint).
2. **Security Scan**: SAST, dependency scanning (pip-audit, npm audit), container scanning (Trivy).
3. **Build & Publish**: Build service images, tag with git SHA, push to registry.
4. **Deploy**: Helm upgrades to dev/staging with manual approvals for production.
5. **Post-Deploy**: Smoke tests, end-to-end regression packs, and metrics verification.

Pipeline definitions (GitHub Actions / GitLab CI) will be published in subsequent commits.


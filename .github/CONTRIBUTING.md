# Contribution Guide

Thank you for your interest in contributing to this project!
Follow these guidelines to have your contribution reviewed and accepted quickly.

## 1. Reporting Issues

- If you find a bug, create an **issue** using the `bug_report.md` template.
- If you want to propose a new feature, create an **issue** using the `feature_request.md` template.
- Be clear, concise, and provide all necessary information to reproduce the problem.

## 2. Setting Up the Local Environment

To contribute, first prepare your development environment:

```bash
# Clone the repository
git clone git@github.com:tyronejosee/project_marketly.git
cd project_marketly

# Create a virtual environment
uv venv

# Install dependencies
uv pip install .

# or
uv pip install -r requirements.txt

# Start services (if using Docker)
docker-compose up -d
````

## 3. Git Workflow

1. Create a **new branch** from `develop` or `main`:

   ```bash
   git checkout develop
   git pull
   git checkout -b feat/new-feature
   ```

2. Make small, clear commits following **Conventional Commits**:

   ```bash
   feat(module): new functionality
   fix(module): bug fix
   refactor(module): refactor without changing behavior
   ```

3. Sync your branch before creating a PR:

   ```bash
   git fetch origin
   git rebase origin/develop
   ```

## 4. Pull Requests

- Open a PR towards `develop`.
- Complete the PR template (`PULL_REQUEST_TEMPLATE.md`).
- Ensure that:

  - All tests pass.
  - Code follows style guidelines (e.g., `black`, `isort`, `ruff`).
  - Documentation is updated if applicable.

## 5. Testing and Code Quality

- Run all tests before creating a PR:

  ```bash
  pytest
  ```

- Check linting and formatting:

  ```bash
  black . --check
  isort . --check-only
  ruff .
  ```

## 6. Code of Conduct

- Be respectful and constructive.
- Keep discussions focused on code, not individuals.
- This project follows a [Code of Conduct](CODE_OF_CONDUCT.md) for contributors.

## 7. Acknowledgements

Thank you for contributing and helping us maintain a clean, safe, and functional project.

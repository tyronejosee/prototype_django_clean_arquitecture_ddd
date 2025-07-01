# ADR 0007: Continuous Integration (CI)

## Context

It is necessary to ensure code quality and automate testing on every change made to the repository.

## Decision

- A continuous integration pipeline will be implemented (for example, using GitHub Actions, GitLab CI, or similar).
- The pipeline will automatically run tests and check code coverage on every push or pull request.
- Steps for linting and automatic code formatting will be included.
- Automatic deployment to staging or production environments may be added in the future.

## Consequences

- Errors and integration failures are detected before merging changes into the main branch.
- A standard of quality and consistency in the code is maintained.
- Collaboration and code review among developers is facilitated.

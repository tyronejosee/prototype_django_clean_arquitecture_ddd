# ADR 0010: Branching Strategy

## Context

A clear and consistent branching strategy is required to facilitate collaboration, code review, and deployment processes. The project must support parallel development, bug fixing, and stable releases.

## Decision

- The `main` branch will always contain the latest stable production-ready code.
- The `develop` branch will be used for ongoing development and integration of new features.
- Feature branches will be created from `develop` and named using the pattern `feature/<short-description>`.
- Bugfix branches will be created from `develop` and named using the pattern `bugfix/<short-description>`.
- Release branches will be created from `develop` when preparing a new production release, named as `release/<version>`.
- Hotfix branches will be created from `main` to quickly address critical issues in production, named as `hotfix/<short-description>`.
- All branches will be merged back into `develop` (and `main` if applicable) through pull requests with code review.
- After a release, the release or hotfix branch will be merged into both `main` and `develop`.

## Consequences

- Parallel development and bug fixing are supported without disrupting the main production branch.
- Code reviews and CI checks are enforced before merging.
- Releases are predictable and traceable.
- The workflow is familiar to most developers and supports automation.

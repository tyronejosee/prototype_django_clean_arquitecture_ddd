# Merge Strategy Guide

This document defines how changes should be merged into the main branches of the repository.

## Main Branches

- `main`: production branch. Must always be stable.
- `develop`: feature integration branch. Merges into `main` only when tested.

## Merge Strategies

1. **Mandatory Pull Requests**
   - All changes to `main` or `develop` must go through a PR.
   - At least **one approved review** is required before merging.

2. **Allowed Merge Types**
   - **Squash merge**: recommended to clean history and combine related commits.
   - **Rebase and merge**: allowed only if the PR contains small, clear commits.
   - **Merge commit**: discouraged, only for release merges if full history is needed.

3. **Commit Messages**
   - Follow **Conventional Commits**:

    ```bash
    feat(module): new functionality
    fix(module): bug fix
    refactor(module): refactor without changing behavior
    ```

   - Avoid generic commits like `Update file`.

## Branch Protection Rules

- `main` and `develop` protected:
  - No direct pushes allowed.
  - CI/CD must pass (tests + linting).
  - Review by at least 1 team member required.
  - Conflicts must be resolved before merging.

## Releases

- Each release is made from `main` using semantic tags (`vX.Y.Z`).
- Creating a release branch is recommended if hotfix or QA is needed before the final merge.

## Additional Notes

- Always sync the branch before creating a PR (`git pull --rebase`).
- Document important changes in the PR.
- PRs should link to an issue if applicable.

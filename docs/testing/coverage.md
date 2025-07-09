# 🛡️ Test Coverage

> [Disclaimer](../DISCLAIMER.md)

## 🎯 Objective

Ensure visibility and control over code quality by measuring the percentage of lines executed by unit, integration, and E2E tests.

## 🧰 Tools

| Tool           | Usage                              |
| -------------- | ---------------------------------- |
| `coverage.py`  | Code coverage analysis             |
| `pytest-cov`   | Plugin for pytest integration      |
| `codecov.io`   | Visual reports in PRs (optional)   |

## 🚦 Coverage Threshold

> **Absolute minimum:** 80% overall, fail CI if below this value.

## 🔧 Useful Commands

```bash
# Run tests with coverage
pytest --cov=apps --cov-report=term-missing

# Generate HTML report
coverage html && open htmlcov/index.html

# Review coverage from terminal
coverage report

# Upload to Codecov (optional)
bash <(curl -s https://codecov.io/bash)
````

## ⚙️ CI Integration

* GitHub Actions runs coverage on every push.
* Optionally integrate `codecov/codecov-action` for visual monitoring.

```yaml
- name: Run tests with coverage
  run: |
    pytest --cov=apps --cov-report=xml

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    token: ${{ secrets.CODECOV_TOKEN }}
```

## ✔️ Best Practices

* Use `# pragma: no cover` for code that should be excluded (e.g., logging).
* Prevent merges if coverage drops.
* Review `term-missing` report for uncovered lines.
* Tests should validate logic, not just executed lines.

## 🔍 Review

* Coverage is reviewed in PRs as part of code review.
* CI fails if coverage falls below threshold.

## 🔮 Future

* Consider branch coverage (`--cov-branch`).
* Separate coverage by test type (unit, integration, E2E).

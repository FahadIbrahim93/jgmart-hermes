# Contributing to JG Mart Hermes

Thank you for your interest in contributing. This project is in active restructuring. Before contributing:

## Code of Conduct
Be respectful. This is a business project serving real customers. Harassment or unprofessional behavior will not be tolerated.

## How to Contribute

### 1. Fork & Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Code Standards
- **Python:** Follow PEP 8, use `black` and `flake8`.
- **JavaScript:** Use Prettier.
- **HTML:** Valid HTML5, accessible (WCAG 2.1 AA).
- **Commits:** Use [Conventional Commits](https://www.conventionalcommits.org/):
  - `feat: add order export API`
  - `fix: resolve dashboard memory leak`
  - `docs: update operations manual`

### 3. Testing
- Add tests for any new logic in `tests/`.
- Run `pytest` before submitting.
- Ensure `black --check .` passes.

### 4. Documentation
- Update `docs/` if you change architecture or add features.
- Update `CHANGELOG.md` for user-facing changes.

### 5. Pull Requests
- Fill out the PR template.
- Link related issues.
- Keep PRs focused — one feature/fix per PR.

## Reporting Issues
Use the bug report or feature request issue templates. For business inquiries, use the investor inquiry template.

## Security
Report security vulnerabilities privately via email to security@jgmart.example (replace with actual contact). Do not open public issues for security flaws.

## License
By contributing, you agree your code will be licensed under the MIT License.

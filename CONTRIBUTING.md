# Contributing to Chemical Equipment Parameter Visualizer

Thank you for your interest in contributing to the Chemical Equipment Parameter Visualizer project!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/chemical-equipment-visualizer.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests to ensure everything works
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py test
```

### Web Frontend
```bash
cd web
npm install
npm run test
npm run dev
```

### Desktop Frontend
```bash
cd desktop
pip install -r requirements.txt
pytest
```

## Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript/React**: Use ESLint and Prettier
- **Commit Messages**: Use clear, descriptive commit messages

## Testing

- Write tests for new features
- Ensure all existing tests pass
- Aim for high test coverage

## Pull Request Guidelines

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Keep PRs focused on a single feature/fix
5. Provide clear description of changes

## Reporting Issues

- Use GitHub Issues
- Provide clear description
- Include steps to reproduce
- Mention your environment (OS, Python/Node version)

## Questions?

Feel free to open an issue for any questions or discussions.

Thank you for contributing!

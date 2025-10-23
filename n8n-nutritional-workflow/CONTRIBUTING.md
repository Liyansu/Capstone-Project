# Contributing to N8N Nutritional Planning Workflow

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, n8n version)
- Screenshots if applicable

### Suggesting Enhancements

We welcome feature suggestions! Please create an issue with:
- Clear description of the feature
- Use case and benefits
- Potential implementation approach
- Examples or mockups if applicable

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow the code style guidelines
   - Add tests for new features
   - Update documentation

4. **Test your changes**
   ```bash
   pytest tests/ -v
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Create a Pull Request**

## 📋 Development Guidelines

### Code Style

**Python:**
- Follow PEP 8 guidelines
- Use type hints where applicable
- Write docstrings for all functions/classes
- Maximum line length: 100 characters

**Example:**
```python
def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation.
    
    Args:
        weight: Weight in kilograms
        height: Height in centimeters
        age: Age in years
        gender: 'male' or 'female'
    
    Returns:
        BMR in kcal/day
    """
    # Implementation here
```

**JavaScript/n8n:**
- Use ES6+ syntax
- Clear variable names
- Comments for complex logic

### Testing

- Write unit tests for all new functions
- Maintain >80% code coverage
- Test edge cases and error handling
- Mock external dependencies

### Documentation

- Update README.md for new features
- Add inline comments for complex logic
- Update API documentation
- Include examples

## 🎯 Priority Areas for Contribution

### High Priority

1. **ML Model Improvements**
   - Fine-tune food recognition models
   - Add new food categories
   - Improve portion estimation accuracy

2. **Database Expansion**
   - Add more meal options
   - Include international cuisines
   - Update nutritional data

3. **Testing**
   - Increase test coverage
   - Add integration tests
   - Performance testing

### Medium Priority

4. **Features**
   - Shopping list generation
   - Recipe recommendations
   - Meal prep planning
   - Progress tracking dashboard

5. **Integrations**
   - Fitness tracker APIs
   - Other messaging platforms
   - Nutrition databases

### Low Priority

6. **UI/UX**
   - Better formatting for Telegram responses
   - Rich media support
   - Interactive buttons

7. **Performance**
   - Caching optimization
   - Model optimization
   - Database query optimization

## 🔍 Code Review Process

All contributions go through review:

1. **Automated Checks**
   - Tests must pass
   - Code style checks
   - Security scans

2. **Manual Review**
   - Code quality
   - Documentation
   - Design patterns
   - Performance implications

3. **Feedback**
   - Address reviewer comments
   - Make requested changes
   - Re-request review

## 📦 Project Structure

```
n8n-nutritional-workflow/
├── nutritional-planning-workflow.json  # n8n workflow
├── python-services/                    # Backend services
│   ├── food_image_analyzer.py         # CV service
│   ├── dietary_planner.py             # Planning service
│   ├── service_launcher.py            # Service starter
│   ├── requirements.txt               # Python deps
│   ├── tests/                         # Test suite
│   │   ├── test_food_analyzer.py
│   │   └── test_dietary_planner.py
│   ├── Dockerfile                     # Container config
│   └── docker-compose.yml             # Multi-container setup
├── README.md                          # Main documentation
├── WORKFLOW_GUIDE.md                  # Technical guide
├── ARCHITECTURE.md                    # System architecture
├── QUICK_START.md                     # Quick setup guide
└── setup.sh                           # Setup script
```

## 🧪 Testing Guidelines

### Unit Tests

```python
import pytest
from dietary_planner import DietaryPlanner

def test_calculate_bmr_male():
    planner = DietaryPlanner()
    bmr = planner.calculate_bmr(75, 175, 30, 'male')
    assert 1690 <= bmr <= 1710
```

### Integration Tests

```python
def test_full_workflow():
    # Test complete workflow from input to output
    user_data = {...}
    result = generate_complete_plan(user_data)
    assert result['success'] is True
    assert 'weekly_plan' in result
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_dietary_planner.py -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

## 🐛 Debugging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test API Endpoints

```bash
# Food analyzer
curl -X POST http://localhost:5000/analyze-food-image \
  -H "Content-Type: application/json" \
  -d '{"image_url": "...", "telegram_file_id": "..."}'

# Dietary planner
curl -X POST http://localhost:5001/generate-meal-plan \
  -H "Content-Type: application/json" \
  -d '{"user_data": {...}}'
```

## 📝 Commit Message Guidelines

Use clear, descriptive commit messages:

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `chore`: Maintenance

**Examples:**
```
feat: Add support for vegetarian meal plans

- Added vegetarian flag to user preferences
- Filtered meat products from meal database
- Updated tests

Closes #123
```

```
fix: Correct BMR calculation for female users

The Mifflin-St Jeor equation was using the wrong
constant for female BMR calculation.

Fixes #456
```

## 🔐 Security

- Never commit API keys or tokens
- Use environment variables for secrets
- Validate all user inputs
- Sanitize data before database queries
- Report security issues privately

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 💬 Communication

- **Issues:** For bugs and feature requests
- **Discussions:** For questions and ideas
- **Pull Requests:** For code contributions

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## ❓ Questions?

Feel free to open an issue or reach out to the maintainers.

Thank you for contributing! 🎉

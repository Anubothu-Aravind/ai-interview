# Contributing to AI Interview System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/ai-interview.git
cd ai-interview
```

3. Set up development environment (see README.md)

## Development Workflow

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes
3. Test your changes thoroughly
4. Commit with clear messages:
```bash
git commit -m "Add: new feature description"
```

5. Push to your fork:
```bash
git push origin feature/your-feature-name
```

6. Create a Pull Request

## Code Style

### Backend (Python)
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions
- Keep functions small and focused
- Use meaningful variable names

Example:
```python
def calculate_score(answer: str, question: str) -> float:
    """
    Calculate the score for an answer.
    
    Args:
        answer: The candidate's answer
        question: The interview question
        
    Returns:
        Score between 0 and 10
    """
    # Implementation
    pass
```

### Frontend (TypeScript/React)
- Use functional components with hooks
- Follow React best practices
- Use TypeScript types strictly
- Keep components small and reusable
- Use meaningful component and variable names

Example:
```typescript
interface Props {
  name: string;
  onSubmit: (data: FormData) => void;
}

const MyComponent: React.FC<Props> = ({ name, onSubmit }) => {
  // Implementation
};
```

## Commit Messages

Use clear, descriptive commit messages:

- `Add:` for new features
- `Fix:` for bug fixes
- `Update:` for updates to existing features
- `Refactor:` for code refactoring
- `Docs:` for documentation changes
- `Test:` for test additions/changes

Examples:
```
Add: voice recording with live transcription
Fix: audio playback not working in Safari
Update: improve error handling in API service
Refactor: extract audio utilities to separate module
Docs: add deployment guide
Test: add unit tests for session manager
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Manual Testing
- Test all user flows end-to-end
- Test on different browsers
- Test with various file formats
- Test error scenarios

## Pull Request Guidelines

1. **Title**: Clear and descriptive
2. **Description**: Explain what and why
3. **Testing**: Describe how you tested
4. **Screenshots**: Include for UI changes
5. **Breaking Changes**: Clearly mark any breaking changes

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How you tested the changes

## Screenshots (if applicable)
Add screenshots here

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No new warnings
- [ ] Changes are backwards compatible
```

## Areas for Contribution

### High Priority
- Add unit tests for backend services
- Add integration tests
- Improve error handling
- Add loading states
- Improve accessibility
- Mobile responsiveness improvements

### Features
- Multi-language support
- Video recording option
- Custom question sets
- Interview scheduling
- Email notifications
- Advanced analytics
- Export to PDF
- Mock interview mode

### Documentation
- API documentation
- Component documentation
- User guide
- Video tutorials
- Troubleshooting guide

## Code Review Process

1. Maintainers will review your PR
2. Address feedback if requested
3. Once approved, PR will be merged
4. Your contribution will be acknowledged

## Questions?

- Open an issue for bugs
- Use discussions for questions
- Tag maintainers for urgent issues

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

Thank you for contributing! 🎉

# Testing Guide

This document provides information on testing the AI Interview System.

## Backend Testing

### Prerequisites
```bash
cd backend
pip install -r requirements.txt
```

### Running Tests

Run all backend tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=backend --cov-report=html
```

Run specific test file:
```bash
pytest backend/test_models.py
pytest backend/test_session_manager.py
pytest backend/test_utils.py
pytest backend/test_api.py
```

Run with verbose output:
```bash
pytest -v
```

### Test Structure

- `test_models.py` - Tests for Pydantic models and data validation
- `test_session_manager.py` - Tests for interview session management
- `test_utils.py` - Tests for utility functions
- `test_api.py` - Tests for API endpoints

### What's Tested

#### Models (`test_models.py`)
- ✅ InterviewSetup validation
- ✅ Question model
- ✅ AnswerSubmission model
- ✅ AnswerEvaluation model
- ✅ QAPair model

#### Session Manager (`test_session_manager.py`)
- ✅ Creating sessions
- ✅ Retrieving sessions
- ✅ Adding conversation history
- ✅ Adding Q&A pairs
- ✅ Deleting sessions

#### Utilities (`test_utils.py`)
- ✅ Text extraction from TXT files
- ✅ File extension validation
- ✅ Case-insensitive validation

#### API (`test_api.py`)
- ✅ Health check endpoint
- ✅ Configuration endpoint
- ✅ Database schema endpoint
- ✅ File upload validation

## Frontend Testing

### Prerequisites
```bash
cd frontend
npm install
```

### Running Tests

Run all frontend tests:
```bash
npm test
```

Run tests in watch mode:
```bash
npm test -- --watch
```

Run tests with coverage:
```bash
npm test -- --coverage
```

### Test Structure

- `App.test.tsx` - Tests for main App component
- `utils/audio.test.ts` - Tests for audio utilities

### What's Tested

#### App Component
- ✅ Renders app title
- ✅ Renders system status
- ✅ Renders how it works section

#### Audio Utilities
- ✅ Time formatting function
- ✅ AudioRecorder instantiation
- ✅ Recording state tracking

## Integration Testing

### Manual Integration Tests

1. **Interview Setup Flow**
   ```
   1. Start backend: ./start-backend.sh
   2. Start frontend: ./start-frontend.sh
   3. Navigate to http://localhost:3000
   4. Fill in candidate details
   5. Upload resume (PDF/TXT)
   6. Upload job description (PDF/TXT)
   7. Click "Start Interview"
   8. Verify session created and first question generated
   ```

2. **Question Delivery**
   ```
   1. Verify question audio plays automatically
   2. Verify question text is displayed
   3. Click "Repeat Question"
   4. Verify repeat counter increments
   5. Wait for repeat window to expire
   6. Verify repeat button is disabled
   ```

3. **Voice Recording**
   ```
   1. Wait for 3-second countdown
   2. Verify recording starts automatically
   3. Speak into microphone
   4. Verify recording timer updates
   5. Verify live transcription appears after 90s
   6. Verify "Stop & Submit" button appears after 90s
   7. Click "Stop & Submit" or wait for auto-submit at 5min
   8. Verify answer is transcribed and evaluated
   ```

4. **Results & History**
   ```
   1. Complete all 10 questions
   2. Verify results screen shows:
      - Overall score
      - Individual question scores
      - Feedback for each answer
   3. Click "Save to Database"
   4. Navigate to History page
   5. Verify interview appears in history
   6. Click on interview to view details
   ```

### API Testing with curl

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Get Configuration
```bash
curl http://localhost:8000/api/v1/config
```

#### Upload Text File
```bash
curl -X POST http://localhost:8000/api/v1/upload/txt \
  -F "file=@/path/to/resume.txt"
```

#### Get Database Schema
```bash
curl http://localhost:8000/api/v1/database/schema
```

## Test Coverage Goals

### Backend
- Models: 100% coverage
- Session Manager: 100% coverage
- Utilities: 100% coverage
- API Endpoints: 80%+ coverage
- OpenAI Service: Integration tests only (mocked)
- Database Service: Integration tests only

### Frontend
- Components: 70%+ coverage
- Utilities: 100% coverage
- Services: 70%+ coverage (mocked API calls)

## CI/CD Testing

Tests should be run in CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
- name: Test Backend
  run: |
    cd backend
    pip install -r requirements.txt
    pytest --cov=backend

- name: Test Frontend
  run: |
    cd frontend
    npm install
    npm test -- --coverage
```

## Known Test Limitations

1. **OpenAI API**: Tests don't call real OpenAI API (too expensive, not deterministic)
2. **Supabase**: Tests don't connect to real database (use mocks)
3. **Audio Recording**: Browser MediaRecorder API requires real browser (not jsdom)
4. **File Upload**: Full end-to-end file upload requires integration testing

## Future Test Additions

- [ ] End-to-end tests with Playwright/Cypress
- [ ] Load testing with Locust
- [ ] Security testing with OWASP ZAP
- [ ] Performance benchmarks
- [ ] Accessibility testing
- [ ] Browser compatibility tests

## Troubleshooting

### Backend Tests Fail

**Problem**: Import errors or module not found
```bash
# Solution: Ensure you're in the project root
cd /path/to/ai-interview
pytest
```

**Problem**: Environment variables missing
```bash
# Solution: Create .env.test file with test values
cp .env.example .env.test
# Edit .env.test with dummy values
```

### Frontend Tests Fail

**Problem**: React Testing Library errors
```bash
# Solution: Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Problem**: Module mock errors
```bash
# Solution: Update jest config in package.json
```

## Test Best Practices

1. **Write tests first** (TDD) when adding new features
2. **Keep tests independent** - each test should run in isolation
3. **Use descriptive names** - test names should explain what they test
4. **Mock external dependencies** - don't call real APIs in unit tests
5. **Test edge cases** - not just happy paths
6. **Keep tests fast** - unit tests should run in milliseconds
7. **Update tests** when changing functionality
8. **Aim for high coverage** but focus on meaningful tests

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Jest documentation](https://jestjs.io/docs/getting-started)

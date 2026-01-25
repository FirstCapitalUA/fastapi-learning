# AGENTS.md

This file contains guidelines and commands for agentic coding agents working in this FastAPI learning repository.

## Build, Lint, and Test Commands

### Development Server
```bash
# Run the FastAPI development server
python main.py
# OR
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Code Quality
```bash
# Run ruff linter (configured in pyproject.toml)
ruff check .

# Run ruff formatter
ruff format .

# Run both lint and format
ruff check . && ruff format .
```

### Testing
This project currently does not have a dedicated test suite. When adding tests:
- Create a `tests/` directory
- Use pytest for testing framework
- Test files should be named `test_*.py` or `*_test.py`
- Run single test: `pytest tests/test_specific.py::test_function`

## Code Style Guidelines

### Project Structure
```
fastapi-learning/
├── core/           # Core functionality (database, config)
├── users/          # User-related modules (models, crud, router)
├── items/          # Item-related modules (models, crud, router)
├── helper/         # Utility functions
├── main.py         # FastAPI app entry point
├── schemas.py      # Shared Pydantic schemas
└── pyproject.toml  # Project configuration
```

### Import Organization
- Standard library imports first
- Third-party imports second (fastapi, sqlmodel, pydantic, etc.)
- Local imports third (relative imports from project modules)
- Use `ruff` for automatic import sorting (configured with `I` rule)

### Type Hints
- Use modern type hints: `str | None` instead of `Optional[str]`
- Use `list[Type]` instead of `List[Type]`
- Use `dict[KeyType, ValueType]` instead of `Dict[KeyType, ValueType]`
- All function parameters and return values should have type hints

### Naming Conventions
- **Variables and functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **File names**: `snake_case.py`
- **Database models**: `PascalCase` (e.g., `User`, `Item`)

### SQLModel/Database Patterns
- Base models inherit from `SQLModel`
- Table models add `table=True` and include primary key: `id: int | None = Field(default=None, primary_key=True)`
- Read models exclude sensitive data (passwords)
- Create models inherit from base models
- Update models use `SQLModel` with optional fields for partial updates
- Use `SessionDep` for database session dependency injection

### FastAPI Router Patterns
- Use `APIRouter` with `prefix` and `tags`
- Import status codes from `starlette.status`
- Return appropriate HTTP status codes:
  - `201_CREATED` for POST/create operations
  - `200_OK` for GET operations
  - `202_ACCEPTED` for DELETE operations
  - `400_BAD_REQUEST` for client errors
  - `404_NOT_FOUND` for missing resources

### Error Handling
- Use `HTTPException` from FastAPI for API errors
- Include descriptive error messages
- Check for `None` values and raise appropriate exceptions
- Use consistent error message format: `"Resource {id} not found"`

### CRUD Operations
- Separate CRUD logic from router logic
- Use descriptive function names: `user_create`, `user_read`, `user_update`, `user_delete`
- Handle database transactions properly: `session.add()`, `session.commit()`, `session.refresh()`
- Return appropriate response models

### Code Formatting
- Line length: 120 characters (configured in ruff)
- Use ruff formatter for consistent formatting
- No trailing whitespace
- Use meaningful variable names

### Configuration
- Use `pydantic_settings.BaseSettings` for configuration
- Store sensitive data in `.env` files
- Use `SettingsConfigDict(env_file=".env", case_sensitive=False)`

### Comments and Documentation
- Use docstrings for complex functions
- Add inline comments for business logic
- Russian comments are acceptable in this learning project
- TODO comments should include actionable items

### Dependencies
- FastAPI with standard extras
- SQLModel for database ORM
- Pydantic for data validation
- Ruff for linting and formatting
- All dependencies managed in `pyproject.toml`

## Ruff Configuration Notes
- Extensive rule set enabled (see pyproject.toml)
- Specific ignores for project patterns
- Per-file ignores for test files
- Builtins ignorelist includes "id"

## Development Workflow
1. Make changes following the style guidelines
2. Run `ruff check .` to fix linting issues
3. Run `ruff format .` to format code
4. Test the API endpoints manually or add tests
5. Ensure all code follows the established patterns

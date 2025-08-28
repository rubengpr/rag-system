# Models Package

This package contains all data models organized by type for better maintainability and clean code principles.

## Structure

```
core/models/
├── __init__.py          # Package exports
├── requests.py          # API request models
├── responses.py         # API response models  
├── internal.py          # Internal business logic models
├── validators.py        # Validation logic (separated from models)
├── example_usage.py     # Usage examples
└── README.md           # This file
```

## Model Categories

### Request Models (`requests.py`)
- **FileUploadRequest**: File upload API requests
- **QueryRequest**: Query API requests with basic field validation

### Response Models (`responses.py`)
- **QueryResponse**: Query API responses
- **UploadResponse**: File upload API responses
- **ChunkInfo**: Text chunk information
- **DocumentInfo**: Document metadata

### Internal Models (`internal.py`)
- **Document**: Internal document representation
- **SearchResult**: Search results with metadata

### Validators (`validators.py`)
- **QueryValidator**: Comprehensive query validation and sanitization

## Key Improvements

### 1. Separation of Concerns
- **Models**: Focus only on data structure and basic validation
- **Validators**: Handle complex validation logic separately
- **Clean interfaces**: Each module has a single responsibility

### 2. Security Validation
- Moved complex security validation from models to dedicated validator
- Comprehensive pattern matching for malicious content
- Configurable validation rules and thresholds

### 3. Maintainability
- Modular structure following project patterns
- Easy to extend and modify individual components
- Clear documentation and examples

## Usage Examples

### Basic Model Usage
```python
from core.models import QueryRequest, QueryResponse

# Create request
request = QueryRequest(query="What is AI?", session_id="123")

# Create response
response = QueryResponse(
    answer="AI is...",
    chunks=[...],
    confidence_score=0.9
)
```

### Validation Usage
```python
from core.models import QueryValidator

validator = QueryValidator()
result = validator.validate_query("What is machine learning?")

if result['is_valid']:
    query = result['sanitized_query']
    # Process query...
else:
    # Handle validation errors
    print(f"Errors: {result['errors']}")
```

### Backward Compatibility
All existing imports continue to work:
```python
from models import QueryRequest, QueryResponse  # Still works
```

## Migration Guide

### For New Code
Use the new modular imports:
```python
from core.models import QueryRequest, QueryResponse, QueryValidator
```

### For Existing Code
No changes needed - backward compatibility is maintained.

### Validation Changes
If you were using Pydantic validators, migrate to the new validator:
```python
# Old way (in model)
@validator('query')
def validate_query(cls, v):
    # Complex validation logic...

# New way (separate validator)
validator = QueryValidator()
result = validator.validate_query(query)
```

## Benefits

1. **Clean Code**: Models focus on structure, validators handle logic
2. **Maintainability**: Easy to modify validation rules without touching models
3. **Testability**: Validators can be tested independently
4. **Extensibility**: Easy to add new validation rules or model types
5. **Security**: Centralized security validation with comprehensive patterns
6. **Performance**: Validation only when needed, not on every model instantiation

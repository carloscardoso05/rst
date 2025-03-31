# RS3 Visualizer

A Python application for parsing and visualizing Rhetorical Structure Theory (RS3) documents. This tool provides an API to access and analyze RS3 files, which contain structured representations of text with rhetorical relationships.

## Features

- Parse RS3 format documents
- Extract rhetorical structures and relationships
- Identify intra-sentential relations
- Process rhetorical signals
- RESTful API for document access and analysis

## Installation

The project uses `uv` for Python package management. Make sure you have Python 3.12 or higher installed.

```bash
# Install dependencies
uv pip install -e .
```

## Core Functionality

### RS3 Parser

The core parser (`core/elements.py`) provides the following functionality:

- Parse RS3 XML documents
- Extract text segments and their relationships
- Identify rhetorical signals
- Process intra-sentential relations
- Handle token management and text extraction

Key classes:
- `RS3Parser`: Main parser class for RS3 documents
- `Node`: Base class for document elements
- `Segment`: Represents text segments
- `Group`: Represents groups of segments
- `Signal`: Represents rhetorical signals
- `Relation`: Represents relationships between elements

### Document Repository

The document repository (`db/documents_repository.py`) manages:
- Document storage and retrieval
- File system operations
- Document metadata management

## API Endpoints

### GET /files/

Lists all available RS3 files in the documents directory.

**Response:**
```json
[
    "filename1.rs3",
    "filename2.rs3",
    ...
]
```

### GET /files/{filename}

Retrieves detailed information about a specific RS3 file.

**Response:**
```json
{
    "file_path": "path/to/file.rs3",
    "intra_sentential_relations": [
        {
            "id": 1,
            "parent_id": 2,
            "relname": "elaboration",
            "text": "example text"
        },
        ...
    ]
}
```

## Development

### Running Tests

The project includes several test commands using `uv`:

```bash
# Run all tests
uv run test

# Run tests in parallel
uv run test-parallel

# Run tests with verbose output
uv run test-verbose

# Run tests in parallel with verbose output
uv run test-parallel-verbose

# Run API tests specifically
uv run test-api

# Run a specific test file
uv run test-file tests/test_api.py

# Run a specific test file in parallel
uv run test-file-parallel tests/test_api.py
```

### Project Structure

```
rst/
├── api/                    # API layer
│   ├── routes/            # API endpoints
│   └── __init__.py
├── core/                  # Core functionality
│   ├── elements.py        # RS3 parser and models
│   └── __init__.py
├── db/                    # Data layer
│   ├── documents_repository.py
│   └── __init__.py
├── documents/            # RS3 document storage
├── tests/               # Test files
└── pyproject.toml       # Project configuration
```

## Dependencies

- Python >= 3.12
- FastAPI
- Pydantic
- pytest
- pytest-xdist
- httpx
<!-- 
## License

[Add your license information here] -->

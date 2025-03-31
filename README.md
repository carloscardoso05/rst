# RST Visualizer

A modern web application for visualizing Rhetorical Structure Theory (RST) relations in documents. This project consists of a FastAPI backend and a Vue.js frontend with Element Plus UI components.

## Project Structure

```
.
├── api/            # Backend FastAPI application
│   └── routes/     # API route handlers
├── db/             # Database and repository layer
├── frontend/       # Vue.js frontend application
│   ├── src/        # Source code
│   └── public/     # Static assets
└── README.md       # This file
```

## Features

- Document list navigation
- RST relation visualization
- Real-time data loading
- Responsive layout
- Error handling and loading states
- Modern UI with Element Plus components

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Setup and Installation

### Backend

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
uvicorn api.main:app --reload --port 8000
```

### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## API Documentation

### Endpoints

- `GET /files`: Get a list of all available documents
- `GET /files/{filename}`: Get RST relations for a specific document

### Response Types

```typescript
interface Relation {
  id: number;
  relname: string | null;
  text: string;
  parent_text: string;
  relation?: {
    type: string;
  };
}

interface DocumentResponse {
  intra_sentential_relations: Relation[];
}
```

## Frontend Architecture

The frontend is built with Vue 3 and TypeScript, using the Composition API. Key components:

- `App.vue`: Main application component
  - Document list navigation
  - Relation visualization
  - Error handling and loading states

### State Management

- Uses Vue's Composition API with `ref` for reactive state
- Handles loading states and error messages
- Manages document selection and relation data

### UI Components

Uses Element Plus components:
- `el-container` for layout
- `el-menu` for document navigation
- `el-card` for content containers
- `el-alert` for error messages
- `el-empty` for empty states

## Development

### Adding New Features

1. Backend:
   - Add new routes in `api/routes/`
   - Update repository layer in `db/`

2. Frontend:
   - Add new components in `frontend/src/components/`
   - Update state management in `App.vue`
   - Add new styles in component's `<style>` section

### Code Style

- Backend: Follow PEP 8 guidelines
- Frontend: Follow Vue.js Style Guide
- Use TypeScript types for all components and functions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[MIT License](LICENSE)

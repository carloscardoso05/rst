# RST Relations Visualizer

A modern web application for visualizing Rhetorical Structure Theory (RST) relations from RS3 files. Built with Vue 3 and TypeScript.

## Features

- Drag and drop RS3 file upload
- Interactive visualization of RST relations
- Filter relations by type (RST and Multinuclear)
- Search functionality for relations
- Detailed view of selected relations
- Modern and responsive UI

## Prerequisites

- Node.js (v16 or higher)
- npm (v7 or higher)

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## Usage

1. Open the application in your web browser
2. Drag and drop RS3 files into the upload area or click to browse
3. Use the filters to show/hide different types of relations
4. Search for specific relations using the search box
5. Click on a relation to view its details

## Development

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Lint code
- `npm run format` - Format code with Prettier

## Project Structure

```
src/
├── components/         # Vue components
├── services/          # Business logic and data processing
├── types/            # TypeScript type definitions
└── App.vue           # Root component
```

## License

MIT 
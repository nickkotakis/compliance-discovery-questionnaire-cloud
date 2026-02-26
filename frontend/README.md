# Compliance Discovery Frontend

React frontend for the Compliance Discovery Questionnaire application.

## Quick Start

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5174`

## Build for Production

```bash
npm run build
```

## Project Structure

```
src/
├── components/
│   └── ComplianceQuestionnaire.tsx  # Main questionnaire component
├── services/
│   └── complianceApi.ts             # API client
├── pages/
│   └── Compliance.tsx               # Main page
├── App.tsx                          # App entry
├── main.tsx                         # React entry
└── index.css                        # Global styles
```

## Configuration

The API endpoint is configured in `src/services/complianceApi.ts`. By default, it connects to `http://localhost:5000`.

To change the API URL, update the `API_BASE_URL` constant:

```typescript
const API_BASE_URL = 'http://localhost:5000';
```

## Features

- Create and manage assessment sessions
- Interactive questionnaire interface
- Real-time progress tracking
- Export templates in multiple formats
- Responsive design

## Technology Stack

- React 18
- TypeScript
- Vite
- Lucide React (icons)

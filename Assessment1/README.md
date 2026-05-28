# Public-API Explorer (Week 1 Assessment)

This is a simple full-stack application built for the Week 1 Assessment.

## Tech Stack
- **Backend:** Python, FastAPI, Pydantic, requests, python-dotenv
- **Frontend:** React, Vite, Vanilla CSS

## Setup Instructions

### Backend (Python)
1. Navigate to the `backend/` folder, install dependencies, and run the FastAPI server:
   ```bash
   cd backend && pip install -r requirements.txt && python main.py
   ```
   *(The API will be available at http://127.0.0.1:5000)*

### Frontend (React + Vite)
1. Navigate to the `frontend/` folder, install dependencies, and start the Vite development server:
   ```bash
   cd frontend && npm install && npm run dev
   ```
   *(The frontend will open in your browser, typically at http://localhost:5173)*

## Features Included
- Fetches data from a public API (`https://jsonplaceholder.typicode.com/posts`) using `requests`.
- Validates the response data using a Pydantic model (`Post`).
- Uses `.env` to load a mock API key to demonstrate `python-dotenv` usage.
- Uses FastAPI to expose an endpoint for the frontend.
- Handles network errors gracefully (simulated with standard error handling).
- Frontend built with React + Vite.
- Includes a reusable `<Card />` component.
- Real-time search/filter functionality filtering through titles and content.
- Elegant loading and error states.
- Premium, modern UI design with hover effects, custom scrollbars, gradients, and custom font.

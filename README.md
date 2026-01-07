# Phase II Full-Stack Todo Application

A production-ready, multi-user todo application with JWT-based authentication and strict user isolation.

## Features

- ✅ User registration and authentication
- ✅ Create tasks with title and description
- ✅ View task list (newest first)
- ✅ Mark tasks as complete/incomplete
- ✅ Edit task details
- ✅ Delete tasks with confirmation
- ✅ Session persistence (7 days)
- ✅ Strict user isolation
- ✅ Responsive design

## Quick Start

See `specs/001-fullstack-todo-app/quickstart.md` for detailed setup instructions.

### Prerequisites
- Python 3.11+
- Node.js 18+
- Neon PostgreSQL account

### Setup
1. Generate JWT secret: `openssl rand -base64 32`
2. Configure `.env` files with BETTER_AUTH_SECRET and DATABASE_URL
3. Run backend: `cd backend && pip install -r requirements.txt && uvicorn src.main:app --reload`
4. Run frontend: `cd frontend && npm install && npm run dev`
5. Visit: http://localhost:3000

## Vercel Deployment

To deploy the frontend on Vercel, follow these steps:

1. Push your code to a GitHub repository
2. Connect your repository to Vercel
3. In the Vercel dashboard, set the following environment variables:
   - `NEXT_PUBLIC_API_URL`: The URL of your deployed backend API (e.g., `https://your-backend-app.vercel.app` or your production backend URL)
   - `BETTER_AUTH_SECRET`: The same JWT secret used in your backend
4. Set the build command to: `cd frontend && npm install && npm run build`
5. Set the output directory to: `frontend/.next`

## Documentation
- Specification: `specs/001-fullstack-todo-app/spec.md`
- Implementation Plan: `specs/001-fullstack-todo-app/plan.md`
- API Contract: `specs/001-fullstack-todo-app/contracts/api-spec.yaml`
- Quickstart Guide: `specs/001-fullstack-todo-app/quickstart.md`

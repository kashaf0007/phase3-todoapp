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

## Production Deployment

### Backend (Hugging Face Space)
Deploy the backend to Hugging Face Spaces:
1. Create a Hugging Face Space with the backend code
2. Configure environment variables:
   - `BETTER_AUTH_SECRET`: Your JWT secret
   - `DATABASE_URL`: Your Neon PostgreSQL connection string
3. The backend will be accessible at: `https://your-username-todo-phase02.hf.space`

### Frontend (Vercel)
Deploy the frontend on Vercel:
1. Push your code to a GitHub repository
2. Connect your repository to Vercel
3. In the Vercel dashboard, set the following environment variables:
   - `NEXT_PUBLIC_API_URL`: Your Hugging Face backend URL (e.g., `https://kashafaman123-todo-phase02.hf.space`)
   - `BETTER_AUTH_SECRET`: The same JWT secret used in your backend
4. Set the build command to: `cd frontend && npm install && npm run build`
5. Set the output directory to: `frontend/.next`

### Important Notes
- Both frontend and backend must use the same `BETTER_AUTH_SECRET`
- The backend is configured to allow CORS requests from `https://hackathon2-phase1-five.vercel.app`
- Make sure both services are deployed and running before testing

## Documentation
- Specification: `specs/001-fullstack-todo-app/spec.md`
- Implementation Plan: `specs/001-fullstack-todo-app/plan.md`
- API Contract: `specs/001-fullstack-todo-app/contracts/api-spec.yaml`
- Quickstart Guide: `specs/001-fullstack-todo-app/quickstart.md`

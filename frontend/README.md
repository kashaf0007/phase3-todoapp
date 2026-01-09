# Todo App Frontend

## Environment Variables

For your Vercel deployment to work properly, you need to set the following environment variable in your Vercel project settings:

- `NEXT_PUBLIC_API_URL`: The URL of your backend API (e.g., https://your-backend-api.com)

## Deployment to Vercel

1. Connect your GitHub repository to Vercel
2. In your Vercel project settings, add the environment variable:
   - Go to your project dashboard on Vercel
   - Navigate to Settings → Environment Variables
   - Add `NEXT_PUBLIC_API_URL` with the URL of your deployed backend API
3. Redeploy your project

## Important Notes

- Make sure your backend API is deployed and accessible from the internet
- The frontend will make API calls to the URL specified in `NEXT_PUBLIC_API_URL`
- If your backend is running locally, it won't be accessible to the deployed frontend
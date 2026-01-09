# Vercel Build Configuration

## Build Output

The following files and directories are created during the build process:

- `.next/` - Next.js build output directory
- `node_modules/` - Dependencies installed during build

## Common Issues and Solutions

1. **Environment Variables Not Set**: 
   - Make sure `NEXT_PUBLIC_API_URL` is set in Vercel environment variables
   - This should point to your deployed backend API

2. **Build Failures**:
   - Check that all dependencies are properly listed in package.json
   - Ensure no development-only dependencies are required for production build

3. **API Connection Issues**:
   - Verify that your backend API is deployed and accessible
   - The frontend deployed on Vercel needs to connect to a publicly accessible backend
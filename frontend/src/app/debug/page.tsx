"use client";

import { useState, useEffect } from "react";

export default function DebugPage() {
  const [envVars, setEnvVars] = useState(null);
  const [apiCheck, setApiCheck] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check environment variables
    const checkEnv = async () => {
      try {
        const response = await fetch('/api/env');
        const data = await response.json();
        setEnvVars(data);
      } catch (error) {
        console.error('Error checking env vars:', error);
      }

      // Check auth configuration
      try {
        const response = await fetch('/api/auth-test');
        const data = await response.json();
        setApiCheck(data);
      } catch (error) {
        console.error('Error checking auth config:', error);
      }

      setLoading(false);
    };

    checkEnv();
  }, []);

  if (loading) {
    return <div className="p-4">Checking configuration...</div>;
  }

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Deployment Debug Info</h1>
      
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">Environment Variables</h2>
        <pre className="bg-gray-100 p-4 rounded overflow-auto">
          {JSON.stringify(envVars, null, 2)}
        </pre>
      </div>
      
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">API Configuration</h2>
        <pre className="bg-gray-100 p-4 rounded overflow-auto">
          {JSON.stringify(apiCheck, null, 2)}
        </pre>
      </div>
      
      <div className="bg-blue-50 p-4 rounded border border-blue-200">
        <h2 className="text-lg font-semibold mb-2">Next Steps</h2>
        <ol className="list-decimal pl-5 space-y-2">
          <li>Ensure NEXT_PUBLIC_API_URL is set in Vercel environment variables</li>
          <li>Your backend API must be publicly accessible</li>
          <li>Redeploy after setting environment variables</li>
        </ol>
      </div>
    </div>
  );
}
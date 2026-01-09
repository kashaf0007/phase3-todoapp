// API route to test authentication configuration
// This helps verify that auth is properly configured for the deployed environment

export async function GET(request: Request) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  
  
  return new Response(
    JSON.stringify({
      status: "success",
      authConfig: {
        apiUrl: apiUrl || "Not set",
        apiUrlSet: !!apiUrl,
      },
      message: "Auth configuration check complete",
    }),
    {
      status: 200,
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
}
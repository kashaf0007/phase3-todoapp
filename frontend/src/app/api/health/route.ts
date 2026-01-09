// This is a simple API route to verify the Next.js app is running
// It's not directly related to your main application but helps verify deployment

export async function GET(request: Request) {
  return new Response(
    JSON.stringify({
      status: "success",
      message: "Frontend app is running on Vercel",
      timestamp: new Date().toISOString(),
    }),
    {
      status: 200,
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
}
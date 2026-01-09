/**
 * Landing Page
 * Redirects based on authentication status
 */

"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-client";

export default function HomePage() {
  const router = useRouter();
  const { user, loading } = useAuth();

  useEffect(() => {
    if (!loading) {
      if (user) {
        // User authenticated - redirect to tasks
        router.push("/tasks");
      } else {
        // User not authenticated - redirect to login
        router.push("/login");
      }
    }
  }, [user, loading, router]);

  // Show loading while checking authentication
  return (
    <div className="task-list-loading">
      <div>Loading...</div>
    </div>
  );
}
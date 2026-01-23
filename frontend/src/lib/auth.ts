/**
 * Better Auth Client Configuration
 * JWT-based authentication for Phase II Todo Application
 */

import { createAuthClient } from "better-auth/react";

/**
 * Better Auth React client
 *
 * Features:
 * - JWT token strategy for stateless authentication
 * - Email/password authentication
 * - Session persistence across browser refreshes
 * - 7-day session duration (per spec Assumption 2)
 */
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:7860",
});

/**
 * Auth hook types for TypeScript
 */
export type User = {
  id: string;
  email: string;
  createdAt: Date;
};

export type Session = {
  user: User;
  token: string;
  expiresAt: Date;
};

/**
 * Get authentication token from session
 * Used for attaching JWT to API requests
 */
export async function getAuthToken(): Promise<string | null> {
  try {
    // Get session using authClient
    const sessionResult = await authClient.$fetch("/api/auth/get-session") as any;
    if (sessionResult?.data) {
      // Extract token from session
      return sessionResult.data.token || null;
    }
    return null;
  } catch (error) {
    console.error("Failed to get auth token:", error);
    return null;
  }
}

/**
 * Clear authentication session
 * Called on logout or 401 errors
 */
export async function clearSession(): Promise<void> {
  try {
    await authClient.signOut();
  } catch (error) {
    console.error("Failed to clear session:", error);
  }
}

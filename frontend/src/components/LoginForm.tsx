'use client';

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import { signIn } from "src/lib/auth-client";

export default function LoginForm() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");

    // Client-side validation
    if (!email || !password) {
      setError("Email and password are required");
      return;
    }

    setLoading(true);

    try {
      // Attempt signin with custom auth client
      await signIn(email, password);

      // Login successful - redirect to tasks page (FR-004, T033)
      router.push("/tasks");
    } catch (err: any) {
      // Handle login errors (FR-003: incorrect credentials)
      if (err.message?.includes("credentials") || err.message?.includes("password")) {
        setError("Incorrect email or password. Please try again.");
      } else if (err.message?.includes("not found")) {
        setError("Account not found. Please sign up first.");
      } else {
        setError(err.message || "Failed to sign in. Please try again.");
      }
      setLoading(false);
    }
  };

  return (
    <div className="auth-form">
      <h1>Sign In</h1>
      <p>Sign in to access your tasks</p>

      <form onSubmit={handleSubmit}>
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            required
            disabled={loading}
            autoComplete="email"
            className="task-form-input"
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            required
            disabled={loading}
            autoComplete="current-password"
            className="task-form-input"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary auth-submit-btn"
        >
          {loading ? "Signing In..." : "Sign In"}
        </button>
      </form>

      <p className="auth-link">
        Don&apos;t have an account?{" "}
        <a href="/signup">Sign up</a>
      </p>
    </div>
  );
}
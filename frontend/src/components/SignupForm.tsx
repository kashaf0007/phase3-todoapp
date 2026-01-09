'use client';

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import { signUp } from "@/lib/auth-client";

export default function SignupForm() {
  const router = useRouter();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");

    // Client-side validation
    if (!name || !email || !password || !confirmPassword) {
      setError("All fields are required");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    setLoading(true);

    try {
      // Attempt signup with custom auth client
      await signUp(email, password, name);

      // Signup successful - redirect to tasks page (FR-004, T033)
      router.push("/tasks");
    } catch (err: any) {
      // Handle signup errors
      if (err.message?.includes("already exists") || err.message?.includes("duplicate")) {
        setError("An account with this email already exists. Please sign in instead.");
      } else {
        setError(err.message || "Failed to create account. Please try again.");
      }
      setLoading(false);
    }
  };

  return (
    <div className="auth-form card bg-white/10 backdrop-blur-lg border border-white/20 shadow-xl">
      <div className="text-center mb-lg">
        <div className="flex justify-center mb-md">
          <div className="bg-primary-100/30 p-md rounded-full backdrop-blur-sm">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-primary-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="40" height="40">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
        </div>
        <h1 className="mb-md text-white">Create Account</h1>
        <p className="text-secondary-200">Join us to manage your tasks efficiently</p>
      </div>

      <form onSubmit={handleSubmit} className="w-full">
        {error && (
          <div className="error-message mb-lg bg-red-500/20 border border-red-400/30 text-red-100 backdrop-blur-sm">
            {error}
          </div>
        )}

        <div className="form-group mb-lg">
          <label htmlFor="name" className="form-label mb-sm text-secondary-200">Full Name</label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter your full name"
            required
            disabled={loading}
            className="form-input w-full bg-white/20 border-white/30 text-white placeholder:text-white/60 focus:border-primary-300 focus:ring focus:ring-primary-300/50"
          />
        </div>

        <div className="form-group mb-lg">
          <label htmlFor="email" className="form-label mb-sm text-secondary-200">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            required
            disabled={loading}
            autoComplete="email"
            className="form-input w-full bg-white/20 border-white/30 text-white placeholder:text-white/60 focus:border-primary-300 focus:ring focus:ring-primary-300/50"
          />
        </div>

        <div className="form-group mb-lg">
          <label htmlFor="password" className="form-label mb-sm text-secondary-200">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Create a password (min 6 characters)"
            required
            disabled={loading}
            autoComplete="new-password"
            className="form-input w-full bg-white/20 border-white/30 text-white placeholder:text-white/60 focus:border-primary-300 focus:ring focus:ring-primary-300/50"
          />
        </div>

        <div className="form-group mb-lg">
          <label htmlFor="confirmPassword" className="form-label mb-sm text-secondary-200">Confirm Password</label>
          <input
            id="confirmPassword"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Confirm your password"
            required
            disabled={loading}
            autoComplete="new-password"
            className="form-input w-full bg-white/20 border-white/30 text-white placeholder:text-white/60 focus:border-primary-300 focus:ring focus:ring-primary-300/50"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary w-full py-3 bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-0.5"
        >
          {loading ? (
            <>
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Creating Account...
            </>
          ) : "Sign Up"}
        </button>
      </form>

      <div className="mt-lg text-center">
        <p className="text-secondary-200">
          Already have an account?{" "}
          <a href="/login" className="text-primary-300 font-medium hover:text-primary-200 transition-colors">
            Sign in
          </a>
        </p>
      </div>
    </div>
  );
}
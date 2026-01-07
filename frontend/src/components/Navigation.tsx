/**
 * Navigation Component
 * Responsive navigation with hamburger menu for mobile devices
 */

"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useAuth, useLogout } from "src/lib/auth-client";
import { useRouter } from "next/navigation";

export function Navigation() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { user, loading } = useAuth();
  const logout = useLogout();
  const router = useRouter();

  // Close menu when route changes
  useEffect(() => {
    const handleRouteChange = () => {
      setIsMenuOpen(false);
    };

    // Note: router.events is not available in Next.js 13+ with App Router
    // We'll handle route changes differently if needed
    return () => {};
  }, [router]);

  // Toggle menu visibility
  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  // Close menu on window resize if it was open
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768 && isMenuOpen) {
        setIsMenuOpen(false);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [isMenuOpen]);

  const handleLogout = async () => {
    await logout();
    router.push('/login');
    setIsMenuOpen(false); // Close menu after logout
  };

  return (
    <nav className="nav-container">
      <div className="nav-content">
        <Link href="/tasks" className="nav-logo">
          Todo App
        </Link>

        {/* Desktop Navigation */}
        <div className="nav-desktop">
          {user && (
            <div className="nav-links">
              <Link href="/tasks" className="nav-link">
                Tasks
              </Link>
            </div>
          )}
          <div className="nav-auth">
            {user ? (
              <button
                onClick={handleLogout}
                className="btn btn-secondary nav-logout-btn"
              >
                Logout
              </button>
            ) : (
              <>
                <Link href="/login" className="nav-link">
                  Login
                </Link>
                <Link href="/signup" className="btn btn-primary nav-signup-btn">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>

        {/* Mobile Menu Button */}
        <div className="nav-mobile">
          <button
            className="nav-menu-btn"
            onClick={toggleMenu}
            aria-label={isMenuOpen ? "Close menu" : "Open menu"}
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="nav-mobile-menu">
          <div className="nav-mobile-content">
            {user ? (
              <>
                <Link href="/tasks" className="nav-mobile-link" onClick={() => setIsMenuOpen(false)}>
                  Tasks
                </Link>
                <button
                  onClick={handleLogout}
                  className="btn btn-secondary nav-mobile-logout"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link href="/login" className="nav-mobile-link" onClick={() => setIsMenuOpen(false)}>
                  Login
                </Link>
                <Link href="/signup" className="btn btn-primary nav-mobile-signup" onClick={() => setIsMenuOpen(false)}>
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
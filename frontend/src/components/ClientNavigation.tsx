'use client';

import { Navigation } from '../components/Navigation';

// Client-only wrapper to ensure Navigation only renders on client side
export default function ClientNavigation() {
  return <Navigation />;
}
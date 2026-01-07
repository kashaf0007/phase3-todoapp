'use client';

import { useState, useRef, ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ClientNavigation from '../components/ClientNavigation';

export default function AppProvider({ children }: { children: ReactNode }) {
  const queryClientRef = useRef<QueryClient | null>(null);

  if (!queryClientRef.current) {
    queryClientRef.current = new QueryClient({
      defaultOptions: {
        queries: {
          staleTime: 5000, // 5 seconds
          retry: 1,
        },
      },
    });
  }

  return (
    <QueryClientProvider client={queryClientRef.current}>
      <div className="app-container">
        <ClientNavigation />
        <main>{children}</main>
      </div>
    </QueryClientProvider>
  );
}
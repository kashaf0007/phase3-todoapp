/**
 * Task List Page
 * Main page for viewing and managing tasks
 */

"use client";

import dynamic from 'next/dynamic';

const AppProviderWithTasks = dynamic(() => import('@/components/AppProviderWithTasks'), { ssr: false });

export default function TasksPage() {
  return <AppProviderWithTasks />;
}

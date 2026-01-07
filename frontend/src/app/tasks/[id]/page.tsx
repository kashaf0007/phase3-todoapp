/**
 * Task Edit Page
 * Edit existing task title and description
 */

"use client";

import dynamic from 'next/dynamic';

const AppProviderWithTaskEdit = dynamic(() => import('@/components/AppProviderWithTaskEdit'), { ssr: false });

export default function TaskEditPage() {
  return <AppProviderWithTaskEdit />;
}

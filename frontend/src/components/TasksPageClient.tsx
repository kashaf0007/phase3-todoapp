'use client';

import { AuthGuard } from "../components/AuthGuard";
import { TaskList } from "../components/TaskList";

export default function TasksPageClient() {
  return (
    <AuthGuard>
      <div className="tasks-container min-h-screen bg-gradient-to-br from-primary-900/20 to-secondary-900/20 pt-8 pb-12">
        <header className="tasks-header px-4">
          <h1 className="text-3xl md:text-4xl font-bold text-white">Welcome To Your Task</h1>
        </header>
        <TaskList />
      </div>
    </AuthGuard>
  );
}
/**
 * TaskList Component
 * Displays list of tasks with loading/error/empty states
 */

"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuth } from "@/lib/auth-client";
import { taskApi } from "@/lib/api";
import { TaskItem } from "./TaskItem";
import { TaskForm } from "./TaskForm";
import type { TaskCreate } from "../types/task";

export function TaskList() {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState("");

  // Fetch tasks using React Query
  const {
    data: tasks,
    isLoading,
    error: fetchError,
  } = useQuery({
    queryKey: ["tasks"],
    queryFn: () => taskApi.list(user?.id || ""),
    enabled: !!user?.id,
  });

  // Create task mutation
  const createMutation = useMutation({
    mutationFn: (newTask: TaskCreate) => taskApi.create(user?.id || "", newTask),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
      setShowForm(false);
      setError("");
    },
    onError: (err: Error) => {
      setError(err.message || "Failed to create task");
    },
  });

  const handleCreateTask = (taskData: TaskCreate) => {
    createMutation.mutate(taskData);
  };

  // Loading state
  if (isLoading) {
    return (
      <div className="task-list-loading flex flex-column justify-center align-center">
        <div className="spinner"></div>
        <p className="mt-md text-secondary-200">Loading your tasks...</p>
      </div>
    );
  }

  // Error state
  if (fetchError) {
    return (
      <div className="card p-lg mt-lg bg-white/10 backdrop-blur-lg border border-white/20 shadow-xl">
        <div className="error-message bg-red-500/20 border border-red-400/30 text-red-100 backdrop-blur-sm">
          Error loading tasks: {(fetchError as Error).message}
        </div>
      </div>
    );
  }

  // Empty state
  if (!tasks || tasks.length === 0) {
    return (
      <div className="task-list-container">
        {!showForm && (
          <div className="task-list-empty flex flex-column justify-center align-center text-center">
            <div className="mb-lg">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-secondary-300 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="64" height="64">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h2 className="mb-md text-white">No tasks yet</h2>
            <p className="text-secondary-200 mb-lg">
              Get started by creating your first task
            </p>
            <button
              onClick={() => setShowForm(true)}
              className="btn btn-primary task-list-create-btn flex align-center justify-center bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-0.5"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="20" height="20">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Create First Task
            </button>
          </div>
        )}

        {showForm && (
          <div className="task-list-form card p-lg bg-white/10 backdrop-blur-lg border border-white/20 shadow-xl">
            {error && (
              <div className="error-message mb-lg bg-red-500/20 border border-red-400/30 text-red-100 backdrop-blur-sm">
                {error}
              </div>
            )}
            <TaskForm
              onSubmit={handleCreateTask}
              onCancel={() => setShowForm(false)}
              loading={createMutation.isPending}
            />
          </div>
        )}
      </div>
    );
  }

  // Task list
  return (
    <div className="task-list-container">
      {!showForm && (
        <div className="mb-lg">
          <button
            onClick={() => setShowForm(true)}
            className="btn btn-primary task-list-add-btn flex align-center justify-center bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-0.5"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="20" height="20">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Add Task
          </button>
        </div>
      )}

      {showForm && (
        <div className="task-list-form card p-lg mb-lg bg-white/10 backdrop-blur-lg border border-white/20 shadow-xl">
          {error && (
            <div className="error-message mb-lg bg-red-500/20 border border-red-400/30 text-red-100 backdrop-blur-sm">
              {error}
            </div>
          )}
          <TaskForm
            onSubmit={handleCreateTask}
            onCancel={() => setShowForm(false)}
            loading={createMutation.isPending}
          />
        </div>
      )}

      <div className="task-list-items">
        {tasks.map((task) => (
          <TaskItem key={task.id} task={task} userId={user?.id || ""} />
        ))}
      </div>
    </div>
  );
}

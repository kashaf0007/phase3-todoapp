/**
 * TaskList Component
 * Displays list of tasks with loading/error/empty states
 */

"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuth } from "src/lib/auth-client";
import { taskApi } from "src/lib/api";
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
      <div className="task-list-loading">
        <div>Loading tasks...</div>
      </div>
    );
  }

  // Error state
  if (fetchError) {
    return (
      <div className="error-message">
        Error loading tasks: {(fetchError as Error).message}
      </div>
    );
  }
  

  // Empty state
  if (!tasks || tasks.length === 0) {
    return (
      <div className="task-list-container">
        {!showForm && (
          <div className="task-list-empty">
            <p className="task-list-empty-text">
              No tasks yet. Create your first task to get started!
            </p>
            <button
              onClick={() => setShowForm(true)}
              className="btn btn-primary task-list-create-btn"
            >
              Create First Task
            </button>
          </div>
        )}

        {showForm && (
          <div className="task-list-form">
            {error && (
              <div className="error-message">
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
        <button
          onClick={() => setShowForm(true)}
          className="btn btn-primary task-list-add-btn"
        >
          Add Task
        </button>
      )}

      {showForm && (
        <div className="task-list-form">
          {error && (
            <div className="error-message">
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

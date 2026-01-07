/**
 * TaskItem Component
 * Individual task display with completion toggle and delete
 */

"use client";

import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { taskApi } from "src/lib/api";
import type { Task } from "../types/task";

interface TaskItemProps {
  task: Task;
  userId: string;
}

export function TaskItem({ task, userId }: TaskItemProps) {
  const queryClient = useQueryClient();
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  // Toggle completion mutation
  const toggleMutation = useMutation({
    mutationFn: () =>
      taskApi.toggleComplete(userId, task.id, { completed: !task.completed }),
    onMutate: async () => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: ["tasks"] });
      const previous = queryClient.getQueryData(["tasks"]);
      queryClient.setQueryData(["tasks"], (old: Task[] | undefined) =>
        old?.map((t) =>
          t.id === task.id ? { ...t, completed: !t.completed } : t
        )
      );
      return { previous };
    },
    onError: (err, variables, context) => {
      // Rollback on error
      queryClient.setQueryData(["tasks"], context?.previous);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: () => taskApi.delete(userId, task.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
      setShowDeleteConfirm(false);
    },
  });

  return (
    <div className={`task-item ${task.completed ? 'task-completed' : ''}`}>
      <div className="task-item-content">
        {/* Completion checkbox */}
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => toggleMutation.mutate()}
          disabled={toggleMutation.isPending}
          className="task-checkbox"
        />

        {/* Task content */}
        <div className="task-details">
          <h3 className={`task-title ${task.completed ? 'completed' : ''}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`task-description ${task.completed ? 'completed' : ''}`}>
              {task.description}
            </p>
          )}
        </div>

        {/* Action buttons */}
        <div className="task-actions">
          <button
            onClick={() => {
              if (typeof window !== "undefined") {
                window.location.href = `/tasks/${task.id}`;
              }
            }}
            className="task-edit-btn"
          >
            Edit
          </button>
          <button
            onClick={() => setShowDeleteConfirm(true)}
            disabled={deleteMutation.isPending}
            className="task-delete-btn"
          >
            {deleteMutation.isPending ? "..." : "Delete"}
          </button>
        </div>
      </div>

      {/* Delete confirmation */}
      {showDeleteConfirm && (
        <div className="task-delete-confirmation">
          <p>Are you sure you want to delete this task?</p>
          <div className="task-delete-actions">
            <button
              onClick={() => deleteMutation.mutate()}
              disabled={deleteMutation.isPending}
              className="btn btn-danger"
            >
              Yes, Delete
            </button>
            <button
              onClick={() => setShowDeleteConfirm(false)}
              disabled={deleteMutation.isPending}
              className="btn btn-secondary"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

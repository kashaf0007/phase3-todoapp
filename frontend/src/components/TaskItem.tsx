/**
 * TaskItem Component
 * Individual task display with completion toggle and delete
 */

"use client";

import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { taskApi } from "@/lib/api";
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
    <div className={`task-item ${task.completed ? 'task-completed' : ''} bg-white/10 backdrop-blur-lg border border-white/20 shadow-lg rounded-xl p-lg transition-all duration-300 hover:shadow-xl`}>
      <div className="task-item-content">
        {/* Completion checkbox */}
        <input
          type="checkbox"
          checked={task.completed}
          onChange={() => toggleMutation.mutate()}
          disabled={toggleMutation.isPending}
          className="task-checkbox w-5 h-5 rounded-md border-2 border-white/30 bg-white/20 checked:bg-primary-500 checked:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-300 focus:ring-opacity-50"
        />

        {/* Task content */}
        <div className="task-details flex-1">
          <h3 className={`task-title ${task.completed ? 'completed text-secondary-300' : 'text-white'} font-semibold text-lg`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`task-description ${task.completed ? 'completed text-secondary-400' : 'text-secondary-200'} text-sm mt-1`}>
              {task.description}
            </p>
          )}
        </div>

        {/* Action buttons */}
        <div className="task-actions flex gap-sm">
          <button
            onClick={() => {
              if (typeof window !== "undefined") {
                window.location.href = `/tasks/${task.id}`;
              }
            }}
            className="btn btn-outline bg-white/20 text-white border-white/30 hover:bg-white/30 hover:border-white/40 transition-all duration-300"
            disabled={toggleMutation.isPending}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-primary-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="16" height="16">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Edit
          </button>
          <button
            onClick={() => setShowDeleteConfirm(true)}
            disabled={deleteMutation.isPending || toggleMutation.isPending}
            className="btn btn-outline bg-white/20 text-white border-white/30 hover:bg-red-500/30 hover:border-red-400/40 transition-all duration-300"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-red-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="16" height="16">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Delete
          </button>
        </div>
      </div>

      {/* Delete confirmation */}
      {showDeleteConfirm && (
        <div className="task-delete-confirmation card p-md mt-md bg-white/10 backdrop-blur-sm border border-white/20 rounded-lg">
          <p className="mb-md text-secondary-200">Are you sure you want to delete this task?</p>
          <div className="task-delete-actions flex gap-md">
            <button
              onClick={() => deleteMutation.mutate()}
              disabled={deleteMutation.isPending}
              className="btn btn-danger flex-1 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white font-semibold shadow-md hover:shadow-lg transition-all duration-300"
            >
              {deleteMutation.isPending ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Deleting...
                </>
              ) : "Yes, Delete"}
            </button>
            <button
              onClick={() => setShowDeleteConfirm(false)}
              disabled={deleteMutation.isPending}
              className="btn btn-secondary flex-1 bg-gradient-to-r from-secondary-500 to-secondary-600 hover:from-secondary-600 hover:to-secondary-700 text-white font-semibold shadow-md hover:shadow-lg transition-all duration-300"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

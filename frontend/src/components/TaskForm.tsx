
/**
 * TaskForm Component
 * Form for creating/editing tasks with validation
 */

"use client";

import { useState, FormEvent } from "react";
import type { TaskCreate } from "../types/task";

interface TaskFormProps {
  onSubmit: (task: TaskCreate) => void;
  onCancel: () => void;
  loading?: boolean;
  initialData?: TaskCreate;
}

export function TaskForm({
  onSubmit,
  onCancel,
  loading = false,
  initialData,
}: TaskFormProps) {
  const [title, setTitle] = useState(initialData?.title || "");
  const [description, setDescription] = useState(initialData?.description || "");
  const [error, setError] = useState("");

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    setError("");

    // Validation
    if (!title.trim()) {
      setError("Title is required");
      return;
    }

    if (title.length > 255) {
      setError("Title must be 255 characters or less");
      return;
    }

    if (description && description.length > 2000) {
      setError("Description must be 2000 characters or less");
      return;
    }

    // Submit
    onSubmit({
      title: title.trim(),
      description: description.trim() || undefined,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="task-form card bg-white/10 backdrop-blur-lg border border-white/20 shadow-xl rounded-xl p-lg">
      {error && (
        <div className="error-message mb-lg bg-red-500/20 border border-red-400/30 text-red-100 backdrop-blur-sm rounded-lg p-md">
          {error}
        </div>
      )}

      <div className="form-group mb-lg">
        <label htmlFor="title" className="form-label mb-sm text-secondary-200">Title *</label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Task title"
          required
          disabled={loading}
          maxLength={255}
          className="form-input w-full bg-white/20 border-white/30 text-white placeholder:text-white/60 focus:border-primary-300 focus:ring focus:ring-primary-300/50 rounded-lg px-3 py-2"
        />
        <div className="flex justify-between mt-sm">
          <small className="text-secondary-300 text-xs">Required</small>
          <small className="char-count text-secondary-300 text-xs">
            {title.length}/255 characters
          </small>
        </div>
      </div>

      <div className="form-group mb-lg">
        <label htmlFor="description" className="form-label mb-sm text-secondary-200">Description (optional)</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Task description"
          disabled={loading}
          maxLength={2000}
          rows={3}
          className="form-input w-full bg-white/20 border-white/30 text-white placeholder:text-white/60 focus:border-primary-300 focus:ring focus:ring-primary-300/50 rounded-lg px-3 py-2"
        />
        <div className="flex justify-between mt-sm">
          <small className="text-secondary-300 text-xs">Optional</small>
          <small className="char-count text-secondary-300 text-xs">
            {description.length}/2000 characters
          </small>
        </div>
      </div>

      <div className="task-form-actions flex gap-md">
        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary flex-1 bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-0.5"
        >
          {loading ? (
            <>
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Saving...
            </>
          ) : "Save Task"}
        </button>
        <button
          type="button"
          onClick={onCancel}
          disabled={loading}
          className="btn btn-secondary flex-1 bg-gradient-to-r from-secondary-500 to-secondary-600 hover:from-secondary-600 hover:to-secondary-700 text-white font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-0.5"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}

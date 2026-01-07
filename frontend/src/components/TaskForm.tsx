
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
    <form onSubmit={handleSubmit} className="task-form">
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <div className="form-group">
        <label htmlFor="title">Title *</label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Task title"
          required
          disabled={loading}
          maxLength={255}
          className="task-form-input"
        />
        <small className="char-count">
          {title.length}/255 characters
        </small>
      </div>

      <div className="form-group">
        <label htmlFor="description">Description (optional)</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Task description"
          disabled={loading}
          maxLength={2000}
          rows={3}
          className="task-form-textarea"
        />
        <small className="char-count">
          {description.length}/2000 characters
        </small>
      </div>

      <div className="task-form-actions">
        <button
          type="submit"
          disabled={loading}
          className="btn btn-success task-form-submit"
        >
          {loading ? "Saving..." : "Save Task"}
        </button>
        <button
          type="button"
          onClick={onCancel}
          disabled={loading}
          className="btn btn-secondary task-form-cancel"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}

/**
 * Toast Notification Utility
 * Simple toast notifications for success/error feedback
 */

type ToastType = "success" | "error" | "info";

interface ToastOptions {
  duration?: number;
  type?: ToastType;
}

/**
 * Show a toast notification
 */
export function showToast(message: string, options: ToastOptions = {}) {
  const { duration = 3000, type = "info" } = options;

  // Create toast container if it doesn't exist
  let container = document.querySelector(".toast-container");
  if (!container) {
    container = document.createElement("div");
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  // Create toast element
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.textContent = message;

  // Add to container
  container.appendChild(toast);

  // Remove after duration
  setTimeout(() => {
    toast.style.animation = "slideOut 0.3s ease-out";
    setTimeout(() => {
      container?.removeChild(toast);

      // Remove container if empty
      if (container?.children.length === 0) {
        document.body.removeChild(container);
      }
    }, 300);
  }, duration);
}

/**
 * Convenience methods
 */
export const toast = {
  success: (message: string) => showToast(message, { type: "success" }),
  error: (message: string) => showToast(message, { type: "error" }),
  info: (message: string) => showToast(message, { type: "info" }),
};

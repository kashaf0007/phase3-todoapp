"""
Fixed Agent orchestration service
"""
from typing import Dict, Any, List
import asyncio
import re
from ...mcp.server import get_mcp_server

class AgentService:
    def __init__(self):
        # Initialize MCP server
        self.mcp_server = get_mcp_server()

    async def process_message_with_agent(self, user_id: str, message: str, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Process a user message with the AI agent and execute MCP tools as needed
        """
        message_lower = message.lower().strip()

        if "add" in message_lower and "task" in message_lower:
            # More robust parsing for task title
            # Match patterns like "add task <title>", "add a task <title>", etc.
            patterns = [
                r"add\s+(?:a\s+)?task\s+(.+)",
                r"create\s+(?:a\s+)?task\s+(.+)",
                r"make\s+(?:a\s+)?task\s+(.+)"
            ]

            title = ""
            for pattern in patterns:
                match = re.search(pattern, message_lower)
                if match:
                    title = match.group(1).strip()
                    break

            # If no pattern matched, try a simpler approach
            if not title:
                # Remove "add" and "task" and surrounding words, then clean up
                title = re.sub(r"\b(add|task|a|an|the)\b", "", message, flags=re.IGNORECASE).strip()
                # Clean up extra whitespace
                title = re.sub(r"\s+", " ", title).strip()

            if not title:
                title = "Untitled task"

            tool_params = {
                "user_id": user_id,
                "title": title,
                "description": f"Task created from message: {message}"
            }

            try:
                # Execute the add_task tool with timeout
                tool_result = await asyncio.wait_for(
                    self.mcp_server.execute_tool("add_task", tool_params),
                    timeout=10.0  # 10 second timeout
                )

                # Check if the tool execution itself failed
                if not tool_result["success"]:
                    error_msg = tool_result.get("error", {}).get("message", "Unknown error")
                    response = f"Sorry, I couldn't add the task: {error_msg}"
                else:
                    # Check if the actual task creation succeeded
                    actual_result = tool_result.get("result", {})
                    if actual_result.get("success") is False:
                        error_msg = actual_result.get("error", {}).get("message", "Unknown error")
                        response = f"Sorry, I couldn't add the task: {error_msg}"
                    else:
                        response = f"I've added the task '{title}' to your list."
            except asyncio.TimeoutError:
                response = f"I'm having trouble connecting to the task service. Your task '{title}' wasn't added."
            except Exception as e:
                response = f"An error occurred while adding your task: {str(e)}"
        elif "list" in message_lower and "task" in message_lower or "show" in message_lower and "task" in message_lower or "my" in message_lower and "task" in message_lower:
            # Execute the list_tasks tool
            tool_params = {
                "user_id": user_id
            }

            try:
                # Execute the list_tasks tool with timeout
                tool_result = await asyncio.wait_for(
                    self.mcp_server.execute_tool("list_tasks", tool_params),
                    timeout=10.0  # 10 second timeout
                )

                # Check if the tool execution itself failed
                if not tool_result["success"]:
                    error_msg = tool_result.get("error", {}).get("message", "Unknown error")
                    response = f"Sorry, I couldn't retrieve your tasks: {error_msg}"
                else:
                    # Check if the actual task listing succeeded
                    actual_result = tool_result.get("result", {})
                    if actual_result.get("success") is False:
                        error_msg = actual_result.get("error", {}).get("message", "Unknown error")
                        response = f"Sorry, I couldn't retrieve your tasks: {error_msg}"
                    else:
                        # Check if the result has the expected structure
                        result_data = actual_result.get("result", {})
                        if "tasks" in result_data:
                            tasks = result_data["tasks"]
                            if tasks:
                                task_list = "\n".join([f"- {task['title']} (ID: {task['id']})" for task in tasks])
                                response = f"Here are your tasks:\n{task_list}"
                            else:
                                response = "You don't have any tasks."
                        else:
                            # If the structure is different, just return an error message
                            response = "You don't have any tasks."
            except asyncio.TimeoutError:
                response = "I'm having trouble connecting to the task service. Couldn't retrieve your tasks."
            except Exception as e:
                response = f"An error occurred while retrieving your tasks: {str(e)}"
        elif "complete" in message_lower or "done" in message_lower or "finish" in message_lower:
            # Extract task ID from message
            task_id_match = re.search(r'\b(\d+)\b', message)
            if task_id_match:
                task_id = int(task_id_match.group(1))

                tool_params = {
                    "user_id": user_id,
                    "task_id": task_id
                }

                try:
                    # Execute the complete_task tool with timeout
                    tool_result = await asyncio.wait_for(
                        self.mcp_server.execute_tool("complete_task", tool_params),
                        timeout=10.0  # 10 second timeout
                    )

                    # Check if the tool execution itself failed
                    if not tool_result["success"]:
                        error_msg = tool_result.get("error", {}).get("message", "Unknown error")
                        response = f"Sorry, I couldn't mark the task as completed: {error_msg}"
                    else:
                        # Check if the actual task completion succeeded
                        actual_result = tool_result.get("result", {})
                        if actual_result.get("success") is False:
                            error_msg = actual_result.get("error", {}).get("message", "Unknown error")
                            response = f"Sorry, I couldn't mark the task as completed: {error_msg}"
                        else:
                            response = f"I've marked the task with ID {task_id} as completed."
                except asyncio.TimeoutError:
                    response = f"I'm having trouble connecting to the task service. Task {task_id} wasn't marked as completed."
                except Exception as e:
                    response = f"An error occurred while marking your task as completed: {str(e)}"
            else:
                response = "I can help mark tasks as complete. Please specify the task ID you want to mark as complete."
        elif "delete" in message_lower or "remove" in message_lower:
            # Extract task ID from message
            task_id_match = re.search(r'\b(\d+)\b', message)
            if task_id_match:
                task_id = int(task_id_match.group(1))

                tool_params = {
                    "user_id": user_id,
                    "task_id": task_id
                }

                try:
                    # Execute the delete_task tool with timeout
                    tool_result = await asyncio.wait_for(
                        self.mcp_server.execute_tool("delete_task", tool_params),
                        timeout=10.0  # 10 second timeout
                    )

                    # Check if the tool execution itself failed
                    if not tool_result["success"]:
                        error_msg = tool_result.get("error", {}).get("message", "Unknown error")
                        response = f"Sorry, I couldn't delete the task: {error_msg}"
                    else:
                        # Check if the actual task deletion succeeded
                        actual_result = tool_result.get("result", {})
                        if actual_result.get("success") is False:
                            error_msg = actual_result.get("error", {}).get("message", "Unknown error")
                            response = f"Sorry, I couldn't delete the task: {error_msg}"
                        else:
                            response = f"I've deleted the task with ID {task_id}."
                except asyncio.TimeoutError:
                    response = f"I'm having trouble connecting to the task service. Task {task_id} wasn't deleted."
                except Exception as e:
                    response = f"An error occurred while deleting your task: {str(e)}"
            else:
                response = "I can help delete tasks. Please specify the task ID you want to delete."
        elif "update" in message_lower or "change" in message_lower or "modify" in message_lower:
            # Extract task ID and new title/description from message
            task_id_match = re.search(r'\b(\d+)\b', message)
            if task_id_match:
                task_id = int(task_id_match.group(1))

                # Extract new title or description from the message
                # Look for patterns like "update task 1 to 'new title'" or "change task 1 description to 'new desc'"
                title_match = re.search(r"(?:to|with title|title is)\s+['\"]([^'\"]+)['\"]", message)
                desc_match = re.search(r"(?:description|desc)\s+(?:to|is)\s+['\"]([^'\"]+)['\"]", message)

                update_params = {
                    "user_id": user_id,
                    "task_id": task_id
                }

                if title_match:
                    update_params["title"] = title_match.group(1)
                if desc_match:
                    update_params["description"] = desc_match.group(1)

                # If no specific update params found, ask for clarification
                if "title" not in update_params and "description" not in update_params:
                    response = f"I can help update the task with ID {task_id}. Please specify what you'd like to change (title or description)."
                else:
                    try:
                        # Execute the update_task tool with timeout
                        tool_result = await asyncio.wait_for(
                            self.mcp_server.execute_tool("update_task", update_params),
                            timeout=10.0  # 10 second timeout
                        )

                        # Check if the tool execution itself failed
                        if not tool_result["success"]:
                            error_msg = tool_result.get("error", {}).get("message", "Unknown error")
                            response = f"Sorry, I couldn't update the task: {error_msg}"
                        else:
                            # Check if the actual task update succeeded
                            actual_result = tool_result.get("result", {})
                            if actual_result.get("success") is False:
                                error_msg = actual_result.get("error", {}).get("message", "Unknown error")
                                response = f"Sorry, I couldn't update the task: {error_msg}"
                            else:
                                response = f"I've updated the task with ID {task_id}."
                    except asyncio.TimeoutError:
                        response = f"I'm having trouble connecting to the task service. Task {task_id} wasn't updated."
                    except Exception as e:
                        response = f"An error occurred while updating your task: {str(e)}"
            else:
                response = "I can help update tasks. Please specify the task ID and what you'd like to change (title or description)."
        else:
            response = f"You said: '{message}'. I can help with tasks using commands like 'add task', 'list tasks', 'show tasks', 'complete task', 'delete task', or 'update task'."

        return {
            "response": response,
            "tool_calls": []
        }
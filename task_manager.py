#!/usr/bin/env python3
"""
Simple Task Manager CLI Application

A command-line task management application that allows users to:
- Add tasks
- List tasks
- Mark tasks as complete
- Delete tasks
- Save/load tasks from a file
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any


class Task:
    """Represents a single task with id, description, completion status, and timestamp."""
    
    def __init__(self, task_id: int, description: str, completed: bool = False):
        self.id = task_id
        self.description = description
        self.completed = completed
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create task from dictionary data."""
        task = cls(data['id'], data['description'], data['completed'])
        task.created_at = data.get('created_at', datetime.now().isoformat())
        return task
    
    def __str__(self) -> str:
        status = "✓" if self.completed else "○"
        return f"[{self.id}] {status} {self.description}"


class TaskManager:
    """Manages a collection of tasks with persistence."""
    
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.next_id = 1
        self.load_tasks()
    
    def add_task(self, description: str) -> Task:
        """Add a new task."""
        task = Task(self.next_id, description)
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        return task
    
    def list_tasks(self, show_completed: bool = True) -> List[Task]:
        """List all tasks, optionally filtering out completed ones."""
        if show_completed:
            return self.tasks
        return [task for task in self.tasks if not task.completed]
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed."""
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self.save_tasks()
                return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False
    
    def save_tasks(self):
        """Save tasks to JSON file."""
        try:
            with open(self.filename, 'w') as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def load_tasks(self):
        """Load tasks from JSON file."""
        if not os.path.exists(self.filename):
            return
        
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(task_data) for task_data in data]
                if self.tasks:
                    self.next_id = max(task.id for task in self.tasks) + 1
        except Exception as e:
            print(f"Error loading tasks: {e}")


def print_help():
    """Print help information."""
    print("""
Task Manager - Simple CLI Task Management

Commands:
  add <description>     Add a new task
  list                  List all tasks
  list-pending          List only pending tasks
  complete <id>         Mark task as completed
  delete <id>           Delete a task
  help                  Show this help message
  quit                  Exit the application

Examples:
  add Buy groceries
  complete 1
  delete 2
""")


def main():
    """Main application loop."""
    print("🔧 Task Manager CLI")
    print("Type 'help' for commands or 'quit' to exit")
    
    manager = TaskManager()
    
    while True:
        try:
            command = input("\n> ").strip().split()
            
            if not command:
                continue
            
            action = command[0].lower()
            
            if action == "quit" or action == "exit":
                print("Goodbye! 👋")
                break
            
            elif action == "help":
                print_help()
            
            elif action == "add":
                if len(command) < 2:
                    print("Usage: add <description>")
                    continue
                description = " ".join(command[1:])
                task = manager.add_task(description)
                print(f"✅ Added task: {task}")
            
            elif action == "list":
                tasks = manager.list_tasks()
                if not tasks:
                    print("No tasks found.")
                else:
                    print(f"\n📋 Tasks ({len(tasks)}):")
                    for task in tasks:
                        print(f"  {task}")
            
            elif action == "list-pending":
                tasks = manager.list_tasks(show_completed=False)
                if not tasks:
                    print("No pending tasks.")
                else:
                    print(f"\n📋 Pending Tasks ({len(tasks)}):")
                    for task in tasks:
                        print(f"  {task}")
            
            elif action == "complete":
                if len(command) != 2:
                    print("Usage: complete <task_id>")
                    continue
                try:
                    task_id = int(command[1])
                    if manager.complete_task(task_id):
                        print(f"✅ Completed task {task_id}")
                    else:
                        print(f"❌ Task {task_id} not found")
                except ValueError:
                    print("❌ Task ID must be a number")
            
            elif action == "delete":
                if len(command) != 2:
                    print("Usage: delete <task_id>")
                    continue
                try:
                    task_id = int(command[1])
                    if manager.delete_task(task_id):
                        print(f"🗑️  Deleted task {task_id}")
                    else:
                        print(f"❌ Task {task_id} not found")
                except ValueError:
                    print("❌ Task ID must be a number")
            
            else:
                print(f"❌ Unknown command: {action}")
                print("Type 'help' for available commands")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except EOFError:
            print("\nGoodbye! 👋")
            break


if __name__ == "__main__":
    main()
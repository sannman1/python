# Python Task Manager Application

A simple command-line task management application built with Python.

## Features

- ✅ Add new tasks
- 📋 List all tasks or pending tasks only
- ✓ Mark tasks as completed
- 🗑️ Delete tasks
- 💾 Automatic saving/loading to JSON file
- 🎨 Clean CLI interface with emojis

## Usage

Run the application:

```bash
python app.py
```

Or run the task manager directly:

```bash
python task_manager.py
```

### Available Commands

- `add <description>` - Add a new task
- `list` - Show all tasks
- `list-pending` - Show only pending tasks
- `complete <id>` - Mark task as completed
- `delete <id>` - Delete a task
- `help` - Show help information
- `quit` - Exit the application

### Example Session

```
🔧 Task Manager CLI
Type 'help' for commands or 'quit' to exit

> add Buy groceries
✅ Added task: [1] ○ Buy groceries

> add Walk the dog
✅ Added task: [2] ○ Walk the dog

> list
📋 Tasks (2):
  [1] ○ Buy groceries
  [2] ○ Walk the dog

> complete 1
✅ Completed task 1

> list
📋 Tasks (2):
  [1] ✓ Buy groceries
  [2] ○ Walk the dog

> quit
Goodbye! 👋
```

## Technical Features

This application demonstrates several Python concepts:

- **Object-Oriented Programming**: Task and TaskManager classes
- **File I/O**: JSON persistence for tasks
- **Error Handling**: Graceful handling of user input and file operations
- **Type Hints**: Modern Python type annotations
- **Command-Line Interface**: Interactive CLI with help system
- **Data Structures**: Lists, dictionaries, and custom objects
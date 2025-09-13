#!/usr/bin/env python3
"""
Basic tests for the Python application
"""

import pytest
import os
import sys
import tempfile

# Add the current directory to Python path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from task_manager import Task, TaskManager
import hello
import app


@pytest.fixture
def temp_task_manager():
    """Create a temporary task manager for testing"""
    temp_file = tempfile.mktemp(suffix='.json')
    manager = TaskManager(temp_file)
    yield manager
    # Cleanup after test
    if os.path.exists(temp_file):
        os.remove(temp_file)


def test_hello_module():
    """Test that hello module can be imported"""
    assert hasattr(hello, '__name__')


def test_app_module():
    """Test that app module can be imported"""
    assert hasattr(app, '__name__')


def test_task_creation():
    """Test creating a basic task"""
    task = Task(1, "Test task")
    assert task.description == "Test task"
    assert task.id == 1
    assert task.completed is False


def test_task_manager_creation():
    """Test creating a task manager"""
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        temp_file = f.name
    try:
        manager = TaskManager(temp_file)
        assert manager is not None
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_task_manager_add_task(temp_task_manager):
    """Test adding a task to task manager"""
    task = temp_task_manager.add_task("Test task")
    assert task.id == 1
    assert len(temp_task_manager.tasks) == 1
    assert temp_task_manager.tasks[0].description == "Test task"


def test_task_manager_complete_task(temp_task_manager):
    """Test completing a task"""
    task = temp_task_manager.add_task("Test task")
    result = temp_task_manager.complete_task(task.id)
    assert result is True
    assert temp_task_manager.tasks[0].completed is True


def test_task_manager_delete_task(temp_task_manager):
    """Test deleting a task"""
    task = temp_task_manager.add_task("Test task")
    result = temp_task_manager.delete_task(task.id)
    assert result is True
    assert len(temp_task_manager.tasks) == 0


if __name__ == "__main__":
    pytest.main([__file__])
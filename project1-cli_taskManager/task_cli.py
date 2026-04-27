import sys
import json
import os
from datetime import datetime

FILE_NAME = "tasks.json"

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []
    
def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(description):
    tasks = load_tasks()
    new_id = 1 if not tasks else max(task["id"] for task in tasks) + 1
    now = datetime.now().isoformat()

    task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }

    tasks.append(task)
    save_tasks(tasks)

    print(f"Task added successfully (ID: {new_id})")

def update_task(task_id, new_description):
    tasks = load_tasks()
    
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print("Task updated successfully")
            return
    
    print("Task not found")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]

    if len(tasks) == len(new_tasks):
        print("Task not found")
        return

    save_tasks(new_tasks)
    print("Task deleted successfully")

def update_status(task_id, status):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task marked as {status}")
            return

    print("Task not found")

def list_tasks(filter_status=None):
    tasks = load_tasks()
    if filter_status not in ["todo", "done", "in-progress"]:
        print("Invalid status")
        return
    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]

    if not tasks:
        print("No tasks found")
        return

    for t in tasks:
        print(f'{[t["id"]]} {t["description"]} ({t["status"]})')

def main():
    args = sys.argv

    if len(args) < 2:
        print("No command provided")
        return

    command = args[1].strip().lower()
    try:
        if command == "add":
            add_task(args[2])

        elif command == "update":
            try:
                task_id = int(args[2])
            except ValueError:
                print("Invalid ID format")
                return

            update_task(task_id, args[3])

        elif command == "delete":
            delete_task(int(args[2]))

        elif command == "mark-in-progress":
            update_status(int(args[2]), "in-progress")

        elif command == "mark-done":
            update_status(int(args[2]), "done")

        elif command == "list":
            if len(args) == 2:
                list_tasks()
            else:
                list_tasks(args[2].lower())

        else:
            print("Unknown command")

    except IndexError:
        print("Missing arguments")
    


if __name__ == "__main__":
    main()
    
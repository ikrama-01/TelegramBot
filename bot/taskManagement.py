from telegram import Update
from telegram.ext import CallbackContext
from dbConn import get_connection
from datetime import datetime
import logging


async def add_task_with_deadline(update, context):
    """Add a task with an optional deadline."""
    try:
        username = context.args[0]
        deadline = " ".join(context.args[-2:])
        task = " ".join(context.args[1:-2])

        if deadline:
            deadline_time = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
            
            if deadline_time <= datetime.now():
                update.message.reply_text("The deadline must be in the future.")
                return
        else:
            deadline_time = None 

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task, deadline, username, status) VALUES (?, ?, ?, ?)",
                       (task, deadline_time, username, 'pending'))
        conn.commit()
        conn.close()

        if deadline_time:
            await update.message.reply_text(f"Task added: {task}, Deadline: {deadline_time}")
        else:
            await update.message.reply_text(f"Task added: {task}, No deadline set.")
        
    except IndexError:
        await update.message.reply_text("Please provide a task and optionally a deadline (e.g., /add_task_with_deadline Finish report 2025-01-17 14:00).")
    except ValueError:
        await update.message.reply_text("The deadline format must be in 'YYYY-MM-DD HH:MM'.")


async def add_task_without_deadline(update, context):
    """Add a task without deadline."""
    try:
        if len(context.args) < 1:
            await update.message.reply_text("Please provide a task description.")
            return
        username = context.args[0]
        task = " ".join(context.args[1:])

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO tasks (task, deadline, username, status) VALUES (?, ?, ?, ?)",
                       (task, None, username, 'pending'))
        conn.commit()
        conn.close()

        await update.message.reply_text(f"Task '{task}' added successfully without a deadline!")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


async def view_tasks(update, context):
    """View all tasks."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT role FROM users WHERE username = ?", (update.effective_user.username,))
        role = cursor.fetchone()
        
        if(role[0] == "Admin" or role[0] == "Manager"):
            cursor.execute("SELECT id, task, status, deadline FROM tasks")
        else:
            cursor.execute("SELECT id, task, status, deadline FROM tasks WHERE username = ?", (update.effective_user.username,))
        
        tasks = cursor.fetchall()

        if tasks:
            task_list = []
            for task in tasks:
                task_id, task_desc, status, deadline = task
                if deadline:
                    task_list.append(f"ID: {task_id} | Task: {task_desc} | Status: {status} | Deadline: {deadline}")
                else:
                    task_list.append(f"ID: {task_id} | Task: {task_desc} | Status: {status} | Deadline: Not Set")
            
            await update.message.reply_text("\n".join(task_list))
        else:
            await update.message.reply_text("You have no tasks.")
        
        conn.close()

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def update_task(update: Update, context: CallbackContext):
    try:
        task_id = int(context.args[0])  
        new_status = context.args[1] 
        username = update.effective_user.username  

        if new_status not in ["pending", "completed"]:
            await update.message.reply_text("Invalid status! Use 'pending' or 'completed'.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ? AND username = ?", (new_status, task_id, username))
        conn.commit()
        conn.close()

        await update.message.reply_text(f"Task {task_id} status updated to {new_status}.")
    except (IndexError, ValueError):
        await update.message.reply_text("Please provide a valid task ID and status (e.g., /update_task 1 completed).")

async def delete_task(update: Update, context: CallbackContext):
    try:
        task_id = int(context.args[0])
        username = update.effective_user.username

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ? AND username = ?", (task_id, username))
        conn.commit()
        conn.close()

        await update.message.reply_text(f"Task {task_id} has been deleted.")
    except (IndexError, ValueError):
        await update.message.reply_text("Please provide a valid task ID (e.g., /delete_task 1).")

logger = logging.getLogger(__name__)

async def view_filtered_tasks(update, context):
    """View filtered tasks based on status."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        filter_status = context.args[0].lower() if context.args else None

        if filter_status: 
            query = "SELECT id, task, status, deadline FROM tasks WHERE status = ?"
            cursor.execute(query, (filter_status,))

        tasks = cursor.fetchall()
        conn.close()

        if tasks:
            task_list = []
            for task in tasks:
                task_id, task_desc, status, deadline = task
                deadline_str = deadline if deadline else "Not Set"
                task_list.append(f"ID: {task_id} | Task: {task_desc} | Status: {status} | Deadline: {deadline_str}")

            await update.message.reply_text("\n".join(task_list))
        else:
            await update.message.reply_text(f"No tasks found with the filter {filter_status if filter_status else 'all'}.")

    except IndexError:
        await update.message.reply_text("Please provide a status to filter by (e.g., /view_filtered_tasks pending). If you want to view all tasks use /view_tasks")
    except Exception as e:
        logger.error(f"Error viewing filtered tasks: {e}")
        await update.message.reply_text(f"Error: {e}")
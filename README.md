# Telegram Bot with Role-Based Access and Task/Subsidiary Management

## Access the Telegram Bot
I have created and hosted the Bot on cloud You can directly access the bot through given Link and please refer to the readme for Bot guide I havent added all the specific details in bot but I have added in readme for testing and assessment purpose, I hope you understand,
Thank You.
Click [here](https://t.me/your_bot_username) to access the bot on Telegram.

---

## Overview

This Telegram bot has been developed for task management, subsidiary management, and role-based access. The bot allows three types of users — **Admin**, **Manager**, and **Employee** — to access different sets of commands based on their roles.

### Features

1. **Role-Based Access Control (RBAC)**:
   - **Admin**: Can access all available commands (view, add, update, delete tasks, subsidiaries).
   - **Manager**: Can manage subsidiaries (view, update) and assign tasks to employees.
   - **Employee**: Can view and update their assigned tasks, view subsidiaries.
   
2. **Task Management**:
   - Create and assign tasks with or without deadlines.
   - View tasks assigned to users.
   - Update and delete tasks.

3. **Subsidiary Management**:
   - Admin and Manager can manage subsidiaries (add, view, update, delete).

---
## How to Explore:
 - Interact with the bot in Telegram using the available commands.
 - Depending on your role, you will have different access to the bot’s features.
 - You can access commands based on your role and explore the functionalities.



## Prerequisites

Ensure you have the following installed:
- Python 3.x
- Telegram Bot API Token
- SQLite (or any other database for persistent storage)

### Dependencies
Install the required libraries via `pip`:
```bash
pip install python-telegram-bot sqlite3
```

---

## How to Set Up the Bot

1. **Clone the Repository**:
   Clone the repository that contains the bot files to your local system.

2. **Set Up Your Telegram Bot**:
   - Create a new bot via [BotFather](https://core.telegram.org/bots#botfather) on Telegram and obtain the **API Token**.
   - Replace `YOUR_API_TOKEN` with your bot's token in the code where the bot is initialized.

3. **Database Setup**:
   - Ensure that the `dbConn.py` file is properly set up for your database connection (SQLite or any other).
   - The bot will store user roles and task/subsidiary data in the database.

---

## Commands and Access Control

### Available Commands

#### Admin
- `/view_users` - View all users and their roles.
- `/add_subsidiary` - Add a new subsidiary.
- `/view_subsidiaries` - View all subsidiaries.
- `/update_subsidiary` - Update an existing subsidiary.
- `/delete_subsidiary` - Delete a subsidiary.
- `/add_task_with_deadline` - Add a task with a deadline.
- `/add_task_without_deadline` - Add a task without a deadline.
- `/view_tasks` - View all tasks.
- `/view_filtered_tasks` - View tasks filtered by status.
- `/update_task` - Update a task.
- `/delete_task` - Delete a task.

#### Manager
- `/view_subsidiaries` - View subsidiaries.
- `/update_subsidiary` - Update a subsidiary.
- `/add_task_with_deadline` - Add a task with a deadline.
- `/add_task_without_deadline` - Add a task without a deadline.
- `/view_tasks` - View tasks.
- `/update_task` - Update a task.

#### Employee
- `/view_subsidiaries` - View subsidiaries.
- `/view_tasks` - View assigned tasks.
- `/update_task` - Update assigned tasks.

---

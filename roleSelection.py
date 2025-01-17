from telegram import InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from dbConn import get_connection

async def start(update, context):
    username = update.effective_user.username
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT role_selected FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and result[0] == 1:  
            await update.message.reply_text("You have already selected your role.")
            return

    except Exception as e:
        print(e)
        await update.message.reply_text(f"Database error: {e}")
        return

    keyboard = [
        [InlineKeyboardButton("Admin", callback_data="Admin")],
        [InlineKeyboardButton("Manager", callback_data="Manager")],
        [InlineKeyboardButton("Employee", callback_data="Employee")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Please choose your role:", reply_markup=reply_markup)

async def handle_role_selection(update, context):
    query = update.callback_query
    await query.answer()
    username = update.effective_user.username
    selected_role = query.data

    if selected_role not in ["Admin", "Manager", "Employee"]:
        await query.edit_message_text("Invalid role selection.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = ?, role_selected = 1 WHERE username = ?", (selected_role, username))
        if cursor.rowcount == 0: 
            cursor.execute("INSERT INTO users (username, role, role_selected) VALUES (?, ?, 1)", (username, selected_role))
        conn.commit()
        conn.close()
        await show_role_commands(query, selected_role)

    except Exception as e:
        await query.edit_message_text(f"Database error: {e}")

async def show_role_commands(query_or_update, role): 
    """Show commands based on role. Accepts both Query and Update objects."""
    if role == "Admin":
        commands = [
            "/view_users", "/add_subsidiary", "/view_subsidiaries", "/update_subsidiary",
            "/delete_subsidiary", "/add_task_without_deadline", "/add_task_with_deadline", "/view_tasks",
            "/view_filtered_tasks", "/update_task", "/delete_task"
        ]
    elif role == "Manager":
        commands = [
            "/view_subsidiaries", "/update_subsidiary", "/add_task_without_deadline","/add_task_with_deadline", "/view_tasks", "/update_task"
        ]
    else: 
        commands = ["/view_subsidiaries", "/view_tasks", "/update_task"]

    keyboard = [[InlineKeyboardButton(cmd, callback_data=cmd)] for cmd in commands]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if isinstance(query_or_update, CallbackQuery): 
        await query_or_update.edit_message_text("Available commands:", reply_markup=reply_markup)
    else:  
        await query_or_update.message.reply_text("Available commands:", reply_markup=reply_markup)


async def help_command(update, context):
    """Handles the /help command."""
    username = update.effective_user.username
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            role = result[0]
            await show_role_commands(update, role)  
        else:
            await update.message.reply_text("Please select a role first using /start.")
    except Exception as e:
        await update.message.reply_text(f"Database error: {e}")

async def view_users(update, context):
    """View all users and their roles."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT username, role FROM users")
        users = cursor.fetchall()
        conn.close()

        if users:
            user_list = "\n".join([f"Username: {username}, Role: {role}" for username, role in users])
            await update.message.reply_text(f"List of all users:\n\n{user_list}")
        else:
            await update.message.reply_text("No users found in the database.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
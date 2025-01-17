from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from dbConn import initialize_database
from taskManagement import *  
from roleSelection import *
from subsidiary import *
from config import BOT_TOKEN

async def handle_inline_button(update, context):
    """Handle inline button presses (paste command)."""
    query = update.callback_query
    await query.answer()  

    command = query.data
    await query.message.reply_text(command)


def main():
    initialize_database()
    app = Application.builder().token(BOT_TOKEN).build()  
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("view_users", view_users))

    app.add_handler(CallbackQueryHandler(handle_role_selection, pattern="^(Admin|Manager|Employee)$"))
    app.add_handler(CallbackQueryHandler(handle_inline_button))  

    # Task Management
    app.add_handler(CommandHandler("add_task_with_deadline", add_task_with_deadline))
    app.add_handler(CommandHandler("add_task_without_deadline", add_task_without_deadline))
    app.add_handler(CommandHandler("view_filtered_tasks", view_filtered_tasks))
    app.add_handler(CommandHandler("view_tasks", view_tasks))
    app.add_handler(CommandHandler("update_task", update_task))
    app.add_handler(CommandHandler("delete_task", delete_task))
    app.add_handler(CommandHandler("help", help_command))

    # Subsidiary management
    app.add_handler(CommandHandler("add_subsidiary", add_subsidiary))
    app.add_handler(CommandHandler("view_subsidiaries", view_subsidiaries))
    app.add_handler(CommandHandler("update_subsidiary", update_subsidiary))
    app.add_handler(CommandHandler("delete_subsidiary", delete_subsidiary))

    app.run_polling()

if __name__ == "__main__":
    main()
from dbConn import get_connection

async def add_subsidiary(update, context):
    try:
        args = context.args
        if len(args) < 4:
            await update.message.reply_text("Usage: /add_subsidiary <name> <location> <manager> <revenue>")
            return

        name, location, manager,revenue = args
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO subsidiaries (name, location, manager, revenue) VALUES (?, ?, ?, ?)", (name, location, manager,revenue))
        conn.commit()
        conn.close()

        await update.message.reply_text(f"Subsidiary '{name}' added successfully!")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def view_subsidiaries(update, context):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, location, manager, revenue FROM subsidiaries")
        subsidiaries = cursor.fetchall()
        conn.close()

        if subsidiaries:
            result = "\n".join(
                [f"ID: {row[0]} | Name: {row[1]} | Location: {row[2]} | Manager: {row[3]} | Revenue: {row[4]}" for row in subsidiaries]
            )
            await update.message.reply_text(result)
        else:
            await update.message.reply_text("No subsidiaries found.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def update_subsidiary(update, context):
    try:
        args = context.args
        if len(args) < 5:
            await update.message.reply_text("Usage: /update_subsidiary <id> <name> <location> <manager> <revenue>")
            return

        id, name, location, manager,revenue = args
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE subsidiaries SET name = ?, location = ?, manager = ?, revenue = ? WHERE id = ?", (name, location, manager,revenue, id))
        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            await update.message.reply_text(f"Subsidiary ID {id} updated successfully!")
        else:
            await update.message.reply_text(f"No subsidiary found with ID {id}.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def delete_subsidiary(update, context):
    try:
        args = context.args
        if len(args) < 1:
            await update.message.reply_text("Usage: /delete_subsidiary <id>")
            return

        id = args[0]
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subsidiaries WHERE id = ?", (id,))
        conn.commit()
        conn.close()

        if cursor.rowcount > 0:
            await update.message.reply_text(f"Subsidiary ID {id} deleted successfully!")
        else:
            await update.message.reply_text(f"No subsidiary found with ID {id}.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

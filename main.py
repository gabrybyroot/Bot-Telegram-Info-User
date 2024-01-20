import mysql.connector
from mysql.connector import Error
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters

TOKEN = ""

user_language = {}

strings = {
    "en": {
        "choose_language": "Please choose your language 🔎:",
        "sender_information": "Your Information",
        "id": "ID Telegram",
        "username": "Username",
        "full_name": "Full Name",
        "forwarded_from_user_information": "Original Sender Information",
        "original_user_id": "Your User ID",
        "original_username": "Your Username",
        "original_full_name": "Your Full Name",
        "language_set": "Language has been set to English.",
        "help": "To use this bot, simply forward a message from any public or private chat and I will provide the available information about the sender. \n\n<b>Command /start /language /help</b>\n\nNote: Not all information may be available due to varying privacy settings. Support chat ➡️ @cyberlinkofficial"
    },
    "it": {
        "choose_language": "Per favore scegli la tua lingua 🔎:",
        "sender_information": "Le tue informazioni",
        "id": "ID Telegram",
        "username": "Tag Telegram",
        "full_name": "Nome e Cognome",
        "forwarded_from_user_information": "Informazioni sul mittente del messaggio",
        "original_user_id": "ID Telegram mittente",
        "original_username": "Tag Telegram mittente",
        "original_full_name": "Nome e Cognome mittente",
        "language_set": "La lingua è stata impostata in Italiano.",
        "help": "Per utilizzare questo bot, basta inoltrare un messaggio da qualsiasi chat pubblica o privata e io fornirò le informazioni disponibili sul mittente. \n\n<b>Comandi /start /language /help</b>\n\nNota: Non tutte le informazioni potrebbero essere disponibili a causa delle diverse impostazioni sulla privacy. Chat di supporto ➡️ @cyberlinkofficial"
    },
    "es": {
        "choose_language": "Por favor, elige tu idioma 🔎:",
        "sender_information": "Tu información",
        "id": "ID de Telegram",
        "username": "Nombre de usuario de Telegram",
        "full_name": "Nombre completo",
        "forwarded_from_user_information": "Información del remitente del mensaje",
        "original_user_id": "ID de Telegram del remitente original",
        "original_username": "Nombre de usuario de Telegram del remitente original",
        "original_full_name": "Nombre completo del remitente original",
        "language_set": "El idioma se ha establecido en español.",
        "help": "Para usar este bot, simplemente reenvía un mensaje desde cualquier chat público o privado y proporcionaré la información disponible sobre el remitente. \n\n<b>Comandos /start /language /help</b>\n\nNota: No toda la información puede estar disponible debido a diferentes configuraciones de privacidad. Soporte en el chat ➡️ @cyberlinkofficial"
    }
}

# Insert your MySQL database details here
DB_HOST = ""
DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""

conn = None

# Connect to the MySQL database
def connect_db():
    try:
        global conn
        conn = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Connected to the MySQL database")
    except Error as e:
        print(e)

# Disconnect from the MySQL database
def disconnect_db():
    if conn and conn.is_connected():
        conn.close()
        print("Disconnected from the MySQL database")

# Update user information in the database
def update_user_info(user_id, username, full_name):
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM UserHistory WHERE telegram_id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if result:
                username_history2 = result[4]
                username_history3 = result[6]
                full_name_history2 = result[5]
                full_name_history3 = result[7]

                if result[2] != username:
                    if not username_history2:
                        username_history2 = username
                    elif not username_history3 and username_history2 != username:
                        username_history3 = username

                if result[3] != full_name:
                    if not full_name_history2:
                        full_name_history2 = full_name
                    elif not full_name_history3 and full_name_history2 != full_name:
                        full_name_history3 = full_name

                query = "UPDATE UserHistory SET username_history3 = %s, full_name_history3 = %s, " \
                        "username_history2 = %s, full_name_history2 = %s " \
                        "WHERE telegram_id = %s"
                cursor.execute(query, (username_history3, full_name_history3,
                                      username_history2, full_name_history2,
                                      user_id))
                conn.commit()
            else:
                query = "INSERT INTO UserHistory (telegram_id, username, full_name) VALUES (%s, %s, %s)"
                cursor.execute(query, (user_id, username, full_name))
                conn.commit()
        except Error as e:
            print(e)
        finally:
            cursor.close()

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.last_name:
        update.effective_message.reply_text(f'Welcome, {user.first_name} {user.last_name}! Type command ➡️ /language to set your language.')
    else:
        update.effective_message.reply_text(f'Welcome, {user.first_name}! Type command ➡️ /language to set your language.')

def language(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data='en'),
            InlineKeyboardButton("Italiano", callback_data='it'),
            InlineKeyboardButton("Spanish", callback_data='es'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_text(strings["en"]["choose_language"], reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_language[query.from_user.id] = query.data
    query.edit_message_text(text=strings[query.data]["language_set"])

def handle_message(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    user_id = update.effective_user.id
    username = update.effective_user.username
    full_name = update.effective_user.full_name
    
    # Update user information in the database
    update_user_info(user_id, username, full_name)
    
    # Information about the original sender of the forwarded message
    original = message.forward_from
    if original:
        original_user_id = original.id
        original_username = original.username
        original_full_name = original.first_name
        if original.last_name:
            original_full_name += " " + original.last_name
            
        # Update information about the original user in the database
        update_user_info(original_user_id, original_username, original_full_name)
        
    # If the user has not set a language, ask them to do so
    if user_id not in user_language:
        language(update, context)
        return

    lang = user_language[user_id]

    sender = message.from_user
    message_info = f" 1️⃣ *{strings[lang]['sender_information']}*\n"
    message_info += f"{strings[lang]['id']}: {sender.id}\n"
    message_info += f"{strings[lang]['username']}: {sender.username if sender.username else 'None'}\n"
    message_info += f"{strings[lang]['full_name']}: {sender.first_name} {sender.last_name if sender.last_name else 'None'}\n"

    # Information about the original sender of the forwarded message
    original = message.forward_from
    
    if original:
        message_info += f"\n 2️⃣ *{strings[lang]['forwarded_from_user_information']}*\n"
        message_info += f"{strings[lang]['original_user_id']}: {original.id}\n"
        message_info += f"{strings[lang]['original_username']}: {original.username if original.username else 'None'}\n"
        message_info += f"{strings[lang]['original_full_name']}: {original.first_name} {original.last_name if original.last_name else 'None'}\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_info, parse_mode=ParseMode.MARKDOWN)

def help_command(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    
    # If the user has not set a language, ask them to do so
    if user_id not in user_language:
        language(update, context)
        return
    lang = user_language[user_id]
    update.effective_message.reply_text(strings[lang]["help"], parse_mode=ParseMode.HTML)

def main() -> None:
    
    # Connect to the MySQL database
    connect_db()
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('language', language))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.forwarded & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()
    
    # Disconnect from the MySQL database
    disconnect_db()

if __name__ == '__main__':
    main()

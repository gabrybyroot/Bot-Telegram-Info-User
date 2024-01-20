# Bot Info User 🤖

The Telegram bot provides user details through forwarded messages and supports setting the preferred language, storing information in a MySQL database.

**Disclaimer:** I do not assume any responsibility for the use of these files by any user. I recommend using them solely for educational, professional, or testing purposes. Feel free to implement the code and make any necessary modifications with comments.

## Description
This Telegram bot facilitates user information retrieval by forwarding any message in public or private chats. Users can set their preferred language (/language) and receive details about the sender, including ID, username, and full name. The bot also tracks the original sender's information in forwarded messages. Language options include English, Italiano, and Spanish. Additionally, the bot stores user details in a MySQL database for historical tracking.

## Dependencies
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)
- [python-telegram-bot](https://pypi.org/project/python-telegram-bot/)


## Install Dependencies
Make sure you have Python installed. You can install the required dependencies using pip:
pip install -r requirements.txt

## Add your token (Line 6)
Make sure to replace "YOUR_BOT_TOKEN" with the actual token provided by BotFather.

## Add your details BD MySQL database (Line 52)
Add your information for the database connection

## Running Bot:
python main.py

## Command Bot Telegram:
- `/start`: Start Info User Bot
  
- `/language`: Set language

- `/help`: Help command

**Note:** Additional information about commands and usage may be available within the bot.




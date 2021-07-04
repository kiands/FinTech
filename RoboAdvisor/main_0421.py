#!/usr/bin/env python

import logging
import telegram

from telegram import Update, ForceReply
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from script import Script

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

Script_handler = Script()
STATUS = "Start"


# Define a few command handlers. These usually take the two arguments update and context.
def start(update, _):
    """Send a message when the command /start is issued."""
    
    update.message.reply_text('hello, {}'.format(update.message.from_user.first_name))
    update.message.reply_text('如果你想要開始投資基金，請輸入/fund')


def help_command(update, _):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')
    update.message.reply_text('如果你想要開始投資基金，請輸入/fund')


def echo(update, _):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def start_script(update, _):
    global Script_handler
    update.message.reply_text('Begin!')
    print(update.message.from_user)
    if update.message.from_user.id in Script_handler.pointer_set:
        print("True")
    else:
        Script_handler.pointer_set[update.message.from_user.id] = 0
        question_1 = Script_handler.Q_set.iloc[0]['question']
        choice = eval(Script_handler.Q_set.iloc[0]['judgement'])
        update.message.reply_text(question_1,reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(qt, callback_data = name) for name, qt in choice.items()]]))
    pass

def script_reply(update, _):
    reply = update.callback_query.data # 一樣從update中抽取資料
    user_id = update.callback_query.from_user.id
    # print(user_id)
    update.callback_query.edit_message_text(text=reply)
    global Script_handler
    next_id = Script_handler.jump_to(user_id)
    if next_id != -1:
        q_type = Script_handler.Q_set.iloc[next_id]['type']
        if q_type == "choice":
            question = Script_handler.Q_set.iloc[next_id]['question']
            choice = eval(Script_handler.Q_set.iloc[next_id]['judgement'])
            update.callback_query.edit_message_text(text=question, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(qt, callback_data = name) for name, qt in choice.items()]]))
            # update.callback_query.edit_message_reply_markup(reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(qt, callback_data = name) for name, qt in choice.items()]]))
        else:
            question = Script_handler.Q_set.iloc[next_id]['question']
            update.callback_query.edit_message_text(text=question)
    else:
        update.callback_query.edit_message_text(text="Finish!")

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1753648492:AAHJA7mz8UCTVicoizQbV8D5MNdSpIImfWE")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Script_handler = Script()

    # on different commands - answer in Telegram

    dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("fund", start_script))

   
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # dispatcher.add_handler(CommandHandler('question', question)) # 問題
    dispatcher.add_handler(CallbackQueryHandler(script_reply)) # 回答問題

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    
    #https://api.telegram.org/bot{$token}/setWebhook?url={$webhook_url}
    #https://api.telegram.org/bot1753648492:AAHJA7mz8UCTVicoizQbV8D5MNdSpIImfWE/setWebhook?url=https://d7e85d05db66.ngrok.io/hook
    #https://d7e85d05db66.ngrok.io

    main()
from telegram.ext import Updater, CommandHandler

import logging

def hello(update, _):
    update.message.reply_text(
        'hello, {}'.format(update.message.from_user.first_name))

def main():
	updater = Updater('1753648492:AAHJA7mz8UCTVicoizQbV8D5MNdSpIImfWE')

	updater.dispatcher.add_handler(CommandHandler('hello', hello))

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':

	#https://api.telegram.org/bot{$token}/setWebhook?url={$webhook_url}
	#https://api.telegram.org/bot1753648492:AAHJA7mz8UCTVicoizQbV8D5MNdSpIImfWE/setWebhook?url=https://b4e6f91df110.ngrok.io/hook
	main()
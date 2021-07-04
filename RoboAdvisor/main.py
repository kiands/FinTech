#!/usr/bin/env python

import logging

from script import Script
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

SALARY, EMERGENCY, EXPEND, INVEST, TARGET, WAY, STATEMENT, PERIOD, STRATEGY, LOSS, RISK = range(11)

Script_handler = Script()

def start(update, _):
    """Send a message when the command /start is issued."""
    
    update.message.reply_text('Hello, {}'.format(update.message.from_user.first_name))
    update.message.reply_text(
        '如果你想要開始投資基金，請輸入 /fund 我們會先為你做個投資風險評估\n'
        '如果你已經完成投資風險評估，請輸入 /result 看看我們為你推薦的基金\n'
    )

def start_script(update, _):
    
    update.message.reply_text('開始!')
    update.message.reply_text('請問您個人的年所得為___萬(請填入正整數)')

    return SALARY

def salary(update, _):

    user = update.message.from_user
    logger.info("Salary of %s: %s", user.first_name, update.message.text)

    try:
        money = int(update.message.text)
    except:
        update.message.reply_text(
        '您未輸入整數 請再試一次',
        reply_markup=ReplyKeyboardRemove(),
        )
        return SALARY
    
    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, SALARY, money)
    
    reply_keyboard = [["無備用金","3個月以下","介於3~6個月","介於6~12個月","超過12個月"]]
    reply_keyboard = [["A","B","C","D","E"]]

    update.message.reply_text(
        '若緊急突發狀況發生時，您的備用金相當於您幾個月的家庭開銷\n'
        'A:無備用金\n'
        'B:3個月以下\n'
        'C:介於3~6個月\n'
        'D:介於6~12個月\n'
        'E:超過12個月\n'
        ,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )

    return EMERGENCY

def emergency(update, _):

    user = update.message.from_user
    logger.info("Emergency of %s: %s", user.first_name, update.message.text)
    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, EMERGENCY, update.message.text)

    reply_keyboard = [["無","100萬（含）以下","100-200萬（含）","200-500萬（含）","500萬（含）以上"]]
    reply_keyboard = [["A","B","C","D","E"]]

    update.message.reply_text(
        '每個月固定支出(償債、生活花費、娛樂等)金額佔所得的佔比\n',
        'A:小於10%\n'
        'B:10-30%\n'
        'C:30-50%\n'
        'D:50-70%\n'
        'E:70%以上\n'
        ,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )

    return EXPEND

def expend(update, _):

    user = update.message.from_user
    logger.info("Expend of %s: %s", user.first_name, update.message.text)

    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, EXPEND, update.message.text)
    
    update.message.reply_text(
        '每個月希望花多少金額在投資：(請填入整數，單位為萬元)',
    )

    return INVEST

def invest(update, _):

    
    user = update.message.from_user
    logger.info("Invest of %s: %s", user.first_name, update.message.text)

    try:
        money = int(update.message.text)
    except:
        update.message.reply_text(
        '您未輸入整數 請再試一次',
        reply_markup=ReplyKeyboardRemove(),
        )
        return INVEST
    
    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, INVEST, money)
    
    update.message.reply_text(
        '您的投資目標是甚麼?',
        reply_markup=ReplyKeyboardRemove(),
    )

    return TARGET

def target(update, _):
   
    user = update.message.from_user
    logger.info("target of %s: %s", user.first_name, update.message.text)
    
    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, TARGET, update.message.text)
    
    update.message.reply_text(
        '投資的方式是哪些呢？\n'
        'A:不曾投資過\n'
        'B:定存\n'
        'C:債券\n'
        'D:基金\n'
        'E:股票\n'
        'F:衍生性金融商品\n'
        ,reply_markup=ReplyKeyboardRemove(),
    )
    
    return WAY


def way(update, _):

    
    user = update.message.from_user
    logger.info("way of %s: %s", user.first_name, update.message.text)

    try:
        answer = update.message.text
        answer_item = "ABCDEFabcdef"
        if len(answer) < 1 or len(answer) > 5:
            update.message.reply_text('回答格式不符1，請再試一次',reply_markup=ReplyKeyboardRemove(),)
            return WAY
        for i in range(len(answer)):
            if answer[i] not in answer_item:
                update.message.reply_text('回答格式不符2，請再試一次',reply_markup=ReplyKeyboardRemove(),)
                return WAY
        answer = answer.upper()
        if "A" in answer and len(answer) > 1:
            update.message.reply_text('回答格式不符3，請再試一次',reply_markup=ReplyKeyboardRemove(),)
            return WAY
        for x in answer:
            if answer.count(x) > 1:
                update.message.reply_text('回答格式不符4，請再試一次',reply_markup=ReplyKeyboardRemove(),)
                return WAY
            
    except:
        update.message.reply_text('請再試一次',reply_markup=ReplyKeyboardRemove(),)
        return WAY
    
    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, WAY, update.message.text)

    reply_keyboard = [["A","B","C"]]
    
    update.message.reply_text(
        '請選擇下列較符合你自身習慣/偏好的敘述\n'
        'A:覺得關注新聞股市及其他投資市場概況很花時間，自己並不想花費心力\n'
        'B:偶爾會關注市場狀況、重要股市新聞\n'
        'C:平時就頻繁在關注國際新聞、股市與其他投資市場概況，認為這樣投資比較安心\n'
        ,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    
    return STATEMENT

def statement(update, _):

    user = update.message.from_user
    logger.info("statement of %s: %s", user.first_name, update.message.text)
    
    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, STATEMENT, update.message.text)
    
    update.message.reply_text(
        '希望＿＿＿＿年可以回收這樣的報酬(請填入正整數)',
        reply_markup=ReplyKeyboardRemove(),
    )

    return PERIOD

def period(update, _):

    
    user = update.message.from_user
    logger.info("period of %s: %s", user.first_name, update.message.text)
    
    try:
        money = int(update.message.text)
        if money <= 0 or money > 100:
            update.message.reply_text(
            '您輸入的整數不在範圍內 請再試一次',
            reply_markup=ReplyKeyboardRemove(),
            )
            return PERIOD
    except:
        update.message.reply_text(
        '您未輸入整數 請再試一次',
        reply_markup=ReplyKeyboardRemove(),
        )
        return PERIOD

    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, PERIOD, money)
    
    reply_keyboard = [["A","B","C","D","E"]]
    
    update.message.reply_text(
        '選擇最適合你的投資策略:(下列選項風險由高至低)\n'
        'A:積極成長型：追求最大的資本利得/利潤\n'
        'B:成長型：追求穩定的成長，追求增值與保值\n'
        'C:平衡型：追求資金的成長與穩定的收益\n'
        'D:收益型：追求定期的收益\n'
        'E:固定收益型：追求穩定的收益\n'
        ,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    
    return STRATEGY

def strategy(update, _):

    user = update.message.from_user
    logger.info("strategy of %s: %s", user.first_name, update.message.text)
    
    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, STRATEGY, update.message.text)
    
    reply_keyboard = [["A","B","C","D","E"]]
    
    update.message.reply_text(
        '當市場有波動而虧損可能採取的處理方式\n'
        'A:全部賣出\n'
        'B:部分賣出\n'
        'C:不賣出\n'
        'D:小部分低檔買進\n'
        'E:大手筆低檔買進\n'
        ,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    
    return LOSS

def loss(update, _):

    
    user = update.message.from_user
    logger.info("loss of %s: %s", user.first_name, update.message.text)
    
    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, LOSS, update.message.text)

    reply_keyboard = [["A","B","C","D"]]
    
    update.message.reply_text(
        '過去的一檔理財產品A在到期後產生的收益超過100%，理財產品B產生的收益超過50%但是運行期間最大損失小於A。如果要在新一輪投資時做一個選擇，您的選擇會是：\n'
        'A:市場環境變了，要重新評估\n'
        'B:重新來，B也沒有A這麼刺激，用B\n'
        'C:A就算再來一次，應該還是很出色，繼續選A\n'
        ,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    
    return RISK

def risk(update, _):

    user = update.message.from_user
    logger.info("risk of %s: %s", user.first_name, update.message.text)
    
    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, STRATEGY, update.message.text)
    
    update.message.reply_text('作答完成', reply_markup=ReplyKeyboardRemove())

    Script_handler.print_answer(update.message.from_user.id)
    Script_handler.save_data()
    return ConversationHandler.END


def cancel(update, _):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('作答結束', reply_markup=ReplyKeyboardRemove())

    # global Script_handler
    # Script_handler.save_data()
    
    return ConversationHandler.END


def main():
    
    global Script_handler
    Script_handler.load_record()
    
    # Create the Updater and pass it your bot's token.
    # updater = Updater("TOKEN")
    updater = Updater("1753648492:AAHJA7mz8UCTVicoizQbV8D5MNdSpIImfWE")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
  
    # SALARY, EMERGENCY, EXPEND, INVEST, TARGET, WAY, STATEMENT, PERIOD, STRATEGY, LOSS, RISK = range(11)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('fund', start_script)],

        states={
            SALARY: [MessageHandler(Filters.text & ~Filters.command, salary)],
            EMERGENCY: [MessageHandler(Filters.regex('^(A|B|C|D|E)$'), emergency)],
            EXPEND: [MessageHandler(Filters.regex('^(A|B|C|D|E)$'), expend)],
            INVEST: [MessageHandler(Filters.text & ~Filters.command, invest)],
            TARGET: [MessageHandler(Filters.text & ~Filters.command, target)],
            WAY: [MessageHandler(Filters.text & ~Filters.command, way)],
            STATEMENT: [MessageHandler(Filters.regex('^(A|B|C)$'), statement)],
            PERIOD: [MessageHandler(Filters.text & ~Filters.command, period)],
            STRATEGY: [MessageHandler(Filters.regex('^(A|B|C|D|E)$'), strategy)],
            LOSS: [MessageHandler(Filters.regex('^(A|B|C|D|E)$'), loss)],
            RISK: [MessageHandler(Filters.regex('^(A|B|C)$'), risk)],
            
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        
    )
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    
    main()

    #https://f3637c589f95.ngrok.io
    #https://api.telegram.org/bot1753648492:AAHJA7mz8UCTVicoizQbV8D5MNdSpIImfWE/setWebhook?url=https://f3637c589f95.ngrok.io/hook
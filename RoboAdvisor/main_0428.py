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

SALARY, DEBT, EXPEND, INVEST, ENTERTAIN, VAR_COST, TARGET, EXPERIENCE, WAY, STATEMENT, PERIOD, STRATEGY, FIX_INTEREST, INTEREST_FREQ, LOSS, EARN, RISK = range(17)

Script_handler = Script()

def start(update, _):
    """Send a message when the command /start is issued."""
    
    update.message.reply_text('Hello, {}'.format(update.message.from_user.first_name))
    update.message.reply_text('如果你想要開始投資基金，請輸入 /fund')

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
    
    reply_keyboard = [["無","100萬（含）以下","100-200萬（含）","200-500萬（含）","500萬（含）以上"]]
    reply_keyboard = [["A","B","C","D","E"]]

    update.message.reply_text(
        '目前擁有的貸款狀況\n'
        'A:無\n'
        'B:100萬（含）以下\n'
        'C:100-200萬（含）\n'
        'D:200-500萬（含）\n'
        'E:500萬（含）以上\n'
        ,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )

    return DEBT

def debt(update, _):

    user = update.message.from_user
    logger.info("Debt of %s: %s", user.first_name, update.message.text)

    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, DEBT, update.message.text)

    update.message.reply_text(
        '每個月固定支出(償債、生活花費、娛樂等)金額佔所得的佔比(請填入0~100間的整數)',
        reply_markup=ReplyKeyboardRemove(),
    )

    return EXPEND

def expend(update, _):

    user = update.message.from_user
    logger.info("Expend of %s: %s", user.first_name, update.message.text)

    try:
        money = int(update.message.text)
        if money <= 0 or money > 100:
            update.message.reply_text(
            '您輸入的整數不在範圍內 請再試一次',
            reply_markup=ReplyKeyboardRemove(),
            )
            return EXPEND
    except:
        update.message.reply_text(
        '您未輸入整數 請再試一次',
        reply_markup=ReplyKeyboardRemove(),
        )
        return EXPEND

    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, EXPEND, money)
    
    update.message.reply_text(
        '每個月希望花收入的多少比例在投資：(請填入0~100間的整數)',
    )

    return INVEST

def invest(update, _):

    
    user = update.message.from_user
    logger.info("Invest of %s: %s", user.first_name, update.message.text)

    try:
        money = int(update.message.text)
        if money <= 0 or money > 100:
            update.message.reply_text('您輸入的整數不在範圍內 請再試一次',reply_markup=ReplyKeyboardRemove(),)
            return INVEST
    except:
        update.message.reply_text('您未輸入整數 請再試一次',reply_markup=ReplyKeyboardRemove(),)
        return INVEST
    
    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, INVEST, money)
    
    reply_keyboard = [["小於10%","10-30%","30-50%","50-70%","70%以上"]]
    reply_keyboard = [["A","B","C","D","E"]]
    
    update.message.reply_text(
        '每個月平均娛樂費用（出遊/看電影/買衣服鞋子等）佔所得比例\n'
        'A:小於10%\n'
        'B:10-30%\n'
        'C:30-50%\n'
        'D:50-70%\n'
        'E:70%以上\n'
        ,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )

    return ENTERTAIN

def entertain(update, _):
    
    
    user = update.message.from_user
    logger.info("Entertain of %s: %s", user.first_name, update.message.text)

    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, ENTERTAIN, update.message.text)

    reply_keyboard = [["1000元以下","1000元（含）~5000元","5000元（含）~5萬元","5萬元~50萬元","50萬元以上"]]
    reply_keyboard = [["A","B","C","D","E"]]
    
    update.message.reply_text(
        '近期花費金額最高的非固定支出金額為______元\n'
        'A:1000元以下\n'
        'B:1000元(含)~5000元\n'
        'C:5000元(含)~5萬元\n'
        'D:5萬元~50萬元\n'
        'E:50萬元以上\n'
        ,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )

    return VAR_COST

def var_cost(update, _):

    user = update.message.from_user
    logger.info("var_cost of %s: %s", user.first_name, update.message.text)
    
    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, VAR_COST, update.message.text)
    
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
    
    reply_keyboard = [["A","B"]]
   
    update.message.reply_text(
        '過去曾投資過嗎\n'
        'A:無\n'
        'B:有\n'
        ,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    
    return EXPERIENCE

def experience(update, _):

    
    user = update.message.from_user
    logger.info("experience of %s: %s", user.first_name, update.message.text)
    
    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, EXPERIENCE, update.message.text)

    reply_keyboard = [["A","B","C","D","E"]]
    
    update.message.reply_text(
        '投資的方式是哪些呢？\n'
        'A:定存\n'
        'B:債券\n'
        'C:基金\n'
        'D:股票\n'
        'E:衍生性金融商品\n'
        ,reply_markup=ReplyKeyboardRemove(),
    )
    
    return WAY

def way(update, _):

    
    user = update.message.from_user
    logger.info("way of %s: %s", user.first_name, update.message.text)

    try:
        answer = update.message.text
        answer_item = "ABCDEabcde"
        if len(answer) < 1 or len(answer) > 5:
            update.message.reply_text('回答格式不符1，請再試一次',reply_markup=ReplyKeyboardRemove(),)
            return WAY
        for i in range(len(answer)):
            if answer[i] not in answer_item:
                update.message.reply_text('回答格式不符2，請再試一次',reply_markup=ReplyKeyboardRemove(),)
                return WAY
        answer = answer.upper()
        for x in answer:
            if answer.count(x) > 1:
                update.message.reply_text('回答格式不符3，請再試一次',reply_markup=ReplyKeyboardRemove(),)
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
    
    reply_keyboard = [["A","B"]]
    
    update.message.reply_text(
        '期望領取固定配息嗎？\n'
        'A:是\n'
        'B:不是\n'
        ,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )

    return FIX_INTEREST

def fix_interest(update, _):

    user = update.message.from_user
    logger.info("fix_interest of %s: %s", user.first_name, update.message.text)
    
    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, FIX_INTEREST, update.message.text)
    
    reply_keyboard = [["A","B","C"]]
    
    update.message.reply_text(
        '配息頻率偏好:\n'
        'A:月配\n'
        'B:季配\n'
        'C:年配\n'
        ,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    
    return INTEREST_FREQ

def interest_freq(update, _):

    
    user = update.message.from_user
    logger.info("interest_freq of %s: %s", user.first_name, update.message.text)
    
    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, INTEREST_FREQ, update.message.text)

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
        '當市場有波動而有利潤時你可能採取的處理模式\n'
        'A:全部賣出\n'
        'B:部分賣出\n'
        'C:不賣出\n'
        'D:加碼買進等待日後繼續漲\n'
        ,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    
    return EARN

def earn(update, _):

    user = update.message.from_user
    logger.info("earn of %s: %s", user.first_name, update.message.text)
    
    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, EARN, update.message.text)
    
    update.message.reply_text('風險與報酬之中，重視風險比例：＿＿＿＿＿％',reply_markup=ReplyKeyboardRemove())
    
    return RISK

def risk(update, _):

    user = update.message.from_user
    logger.info("risk of %s: %s", user.first_name, update.message.text)
    
    try:
        money = int(update.message.text)
        if money <= 0 or money > 100:
            update.message.reply_text('您輸入的整數不在範圍內 請再試一次',reply_markup=ReplyKeyboardRemove(),)
            return RISK
    except:
        update.message.reply_text('您未輸入整數 請再試一次',reply_markup=ReplyKeyboardRemove(),)
        return RISK

    global Script_handler
    Script_handler.save_answer(update.message.from_user.id, RISK, money)
    
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

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('fund', start_script)],

        states={
            SALARY: [MessageHandler(Filters.text & ~Filters.command, salary)],
            DEBT: [MessageHandler(Filters.regex('^(A|B|C|D|E)$'), debt)],
            EXPEND: [MessageHandler(Filters.text & ~Filters.command, expend)],
            INVEST: [MessageHandler(Filters.text & ~Filters.command, invest)],
            ENTERTAIN: [MessageHandler(Filters.regex('^(A|B|C|D|E)$'), entertain)],
            VAR_COST: [MessageHandler(Filters.regex('^(A|B|C|D|E)$'), var_cost)],
            TARGET: [MessageHandler(Filters.text & ~Filters.command, target)],
            # EXPERIENCE: [MessageHandler(Filters.regex('^(A|B)$'), experience)],
            EXPERIENCE: [MessageHandler(Filters.regex('^(A)$'), way),MessageHandler(Filters.regex('^(B)$'), experience)],
            # WAY: [MessageHandler(Filters.regex('^(A|B|C|D|E)$'), way)],
            WAY: [MessageHandler(Filters.text & ~Filters.command, way)],
            STATEMENT: [MessageHandler(Filters.regex('^(A|B|C)$'), statement)],
            PERIOD: [MessageHandler(Filters.text & ~Filters.command, period)],
            STRATEGY: [MessageHandler(Filters.regex('^(A|B|C|D|E)$'), strategy)],
            FIX_INTEREST: [MessageHandler(Filters.regex('^(A|B)$'), fix_interest)],
            INTEREST_FREQ: [MessageHandler(Filters.regex('^(A|B|C)$'), interest_freq)],
            LOSS: [MessageHandler(Filters.regex('^(A|B|C|D|E)$'), loss)],
            EARN: [MessageHandler(Filters.regex('^(A|B|C|D)$'), earn)],
            RISK: [MessageHandler(Filters.text & ~Filters.command, risk)],
            
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
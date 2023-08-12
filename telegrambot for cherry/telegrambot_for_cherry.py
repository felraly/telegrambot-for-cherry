from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# 텔레그램 봇의 토큰을 입력하세요
TOKEN = '6321575706:AAFdH-lVl5r3Ai0DhFlQHsyt_mK0dpakMnc'

def start(update, context):
    update.message.reply_text('안녕하세요! /warn을 입력하면 "노" 관련 메시지에 경고가 출력됩니다.')

def warn(update, context):
    update.message.reply_text('경고: "노" 관련 메시지가 감지되었습니다!')

def message_handler(update, context):
    text = update.message.text.lower()
    if text.endswith('노'):
        update.message.reply_text('/warn')

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('warn', warn))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

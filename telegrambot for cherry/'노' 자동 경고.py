# -*- coding: utf-8 -*-
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters



# 텔레그램 봇의 토큰을 입력하세요
TOKEN = '6112482376:AAHkF-Exg8lerMiOXrorViF1FwXEzw6HPPA'

def start(update, context):
    update.message.reply_text('안녕하세요! "노" 관련 메시지에 경고가 출력됩니다.')

def message_handler(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    if text.endswith('노'):
        update.message.reply_text('/warn')

def test(update: Update, context: CallbackContext):
    user_name = update.message.from_user.name
    update.message.reply_text(f'/warn {user_name}')

# 메인 함수
def main():
    # 로깅 설정
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def main():
    updater = Updater(token=TOKEN, use_context=True, request_kwargs={'read_timeout': 6, 'connect_timeout': 7})
    dp = updater.dispatcher
    

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))
    dp.add_handler(CommandHandler('test', test))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
# 이 위는 인코딩형식을 지정하는 함수로 건드리지 말 것
# 만약 인코딩이 깨졌다면  맨 윗줄을 -*- coding: eur-kr -*- 로 바꾸고 다시 실행해보기

import logging
import re
import datetime
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters



# 텔레그램 봇의 토큰을 입력하세요
TOKEN = '6112482376:AAHkF-Exg8lerMiOXrorViF1FwXEzw6HPPA'

def remove_special_characters(text):
    # 정규 표현식을 사용하여 특수 문자 제거
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    return cleaned_text

def start(update, context):
    update.message.reply_text('@JunetoAugust @Cherry902040 @RyjiOlllllllllllllllllllllllllll @Ahndangdang')
    
def message_handler(update: Update, context: CallbackContext):
    original_text = update.message.text
    cleaned_text = remove_special_characters(original_text)
    text = update.message.text.lower()
    now = datetime.datetime.now()
    if now.hour >= 8 and now.hour < 24:
        if cleaned_text.endswith('노') and not cleaned_text.endswith('야노'): 
            update.message.reply_text('@MAVE_RICK_114 \n 너... 썼구나...?')
       
    elif now.hour >= 0 and now.hour < 3:
        if cleaned_text.endswith('노') and not cleaned_text.endswith('야노'): 
            update.message.reply_text('@MAVE_RICK_114 \n 너... 썼구나...?')
       
    elif now.hour >= 3 and now.hour < 7:
        if cleaned_text.endswith('노') and not cleaned_text.endswith('야노'): 
            update.message.reply_text('@MAVE_RICK_114 \n 너... 썼구나...?')
            
    elif now.hour >= 7 and now.hour < 8:
        if cleaned_text.endswith('노') and not cleaned_text.endswith('야노'): 
            update.message.reply_text('@MAVE_RICK_114 \n 너... 썼구나...?')
       
       # now.hour는 시간대에 따라 다른 동작을 나타낼때 쓰는 함수
       # cleaned_text.endswith는 끝에 끝나는 글자를 금지할때 쓰는 함수
       # and not뒤 부터는 예외를 지정함
       # 예외를 추가 할땐 and not text.endswith('야노')와 같이 작성하기
       # 출력될 텍스트를 입력하세요,\n 뒤는 줄바꿈 되어서 출력됨
       

    
# 여기는 건드리지 말 것
# 메인 함수

    # 로깅 설정
    

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(token=TOKEN, use_context=True, request_kwargs={'read_timeout': 6, 'connect_timeout': 7})
    dp = updater.dispatcher
    

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

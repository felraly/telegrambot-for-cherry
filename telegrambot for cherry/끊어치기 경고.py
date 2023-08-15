import re
from telegram import Update
import logging
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

TOKEN = '6112482376:AAHkF-Exg8lerMiOXrorViF1FwXEzw6HPPA'
MESSAGE_LIMIT = 3  # 메시지 수 제한
TEXT_LIMIT = 15    # 텍스트 길이 제한

def update_chat_stats(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

def remove_special_chars(text):
    return re.sub(r'[^\w\s]', '', text)  # 특수 문자 제거

def warn(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if 'message_count' not in context.user_data:
        context.user_data['message_count'] = 0
    
    context.user_data['message_count'] += 1
    if context.user_data['message_count'] >= MESSAGE_LIMIT:
        total_text_length = sum(len(msg.text) for msg in context.user_data['messages'])
        if total_text_length <= TEXT_LIMIT:
            update.message.reply_text('/warn \n 좀 하지 말라면 하지 말라고')
        
        context.user_data['message_count'] = 0
        context.user_data['messages'] = []

    context.user_data.setdefault('messages', []).append(update.message)

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(MessageHandler(Filters.text, warn))
    dp.add_handler(MessageHandler(Filters.text | Filters.photo | Filters.document | Filters.audio, update_chat_stats))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()




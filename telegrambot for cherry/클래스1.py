from telegram import Update
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import requests
from bs4 import BeautifulSoup

TOKEN = '6112482376:AAHkF-Exg8lerMiOXrorViF1FwXEzw6HPPA'

START_DATE = ''
END_DATE = ''
MAX_CHAT_COUNT = 100
CHOOSING, SETTING_PARAMS = range(2)

# "/start" 명령어 제거
def main_menu(update: Update, context: CallbackContext):
    update.message.reply_text("사용자 이름을 가져오려면 /get_names 명령어를 사용하세요.")
    return CHOOSING

def set_params(update: Update, context: CallbackContext):
    global START_DATE, END_DATE, MAX_CHAT_COUNT
    params = context.args

    if len(params) != 3:
        update.message.reply_text("올바른 형식으로 설정하세요. (예: /set_params 날짜1 날짜2 채팅수)")
        return CHOOSING

    START_DATE, END_DATE, MAX_CHAT_COUNT = params[0], params[1], int(params[2])
    update.message.reply_text(f"날짜 범위가 {START_DATE}부터 {END_DATE}, 채팅 수가 {MAX_CHAT_COUNT} 이하로 설정되었습니다.")

    return CHOOSING

def get_names(update: Update, context: CallbackContext):
    global START_DATE, END_DATE, MAX_CHAT_COUNT
    if not START_DATE or not END_DATE or MAX_CHAT_COUNT < 0:
        update.message.reply_text("먼저 날짜 범위 및 채팅 수를 설정하세요. (예: /set_params 날짜1 날짜2 채팅수)")
        return CHOOSING

    url = 'https://combot.org/c/1927829363'

    # 웹페이지 가져오기
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        user_names = []

        # 설정한 조건에 맞는 사용자 추출
        for user_div in soup.find_all('div', class_='user-info'):
            username = user_div.find('span', class_='username').text
            chat_count = int(user_div.find('span', class_='chat-count').text)
            date = user_div.find('span', class_='date').text
            if chat_count <= MAX_CHAT_COUNT and START_DATE <= date <= END_DATE:
                user_names.append(username)

        if user_names:
            message = f"날짜 범위 {START_DATE}부터 {END_DATE}, 채팅 수가 {MAX_CHAT_COUNT} 이하인 사용자:\n"
            for username in user_names:
                message += f"{username}\n"
        else:
            message = f"날짜 범위 {START_DATE}부터 {END_DATE}, 채팅 수가 {MAX_CHAT_COUNT} 이하인 사용자가 없습니다."

        update.message.reply_text(message)
    else:
        update.message.reply_text('웹페이지에 접근할 수 없습니다.')

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    
    # "/start" 명령어 대신 "main_menu" 함수를 사용
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', main_menu)],
        states={
            CHOOSING: [CommandHandler('set_params', set_params, pass_args=True), CommandHandler('get_names', get_names)],
        },
        fallbacks=[]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('set_params', set_params, pass_args=True))
    dp.add_handler(CommandHandler('get_names', set_params, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()





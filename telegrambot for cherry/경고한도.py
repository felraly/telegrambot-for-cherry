from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = '6112482376:AAHkF-Exg8lerMiOXrorViF1FwXEzw6HPPA'

# 그룹별 경고한도 저장
GROUP_LIMITS = {}

# 경고 한도 설정 함수
def set_group_limit(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    user_status = context.bot.get_chat_member(chat_id, user_id).status

    if user_status != 'creator':
        update.message.reply_text('그룹 소유자만 설정을 변경할 수 있습니다.')
        return

    try:
        limit = int(context.args[0])
        GROUP_LIMITS[chat_id] = limit
        update.message.reply_text(f'그룹의 경고한도가 {limit}로 설정되었습니다.')
    except (IndexError, ValueError):
        update.message.reply_text('올바른 형식으로 그룹의 경고한도를 설정해주세요.\n예: /limit 3')

# 현재 설정된 경고 한도 확인 함수
def get_group_limit(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    current_limit = GROUP_LIMITS.get(chat_id)

    if current_limit is not None:
        update.message.reply_text(f'현재 그룹의 경고한도는 {current_limit}입니다.')
    else:
        update.message.reply_text('아직 그룹의 경고한도가 설정되지 않았습니다.')

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('limit', set_group_limit, pass_args=True))
    dp.add_handler(CommandHandler('get_limit', get_group_limit))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

from cgitb import text
from telegram import Update, ParseMode
import logging
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

TOKEN = '6112482376:AAHkF-Exg8lerMiOXrorViF1FwXEzw6HPPA'
GROUP_LIMITS = {}  # 그룹별 경고한도를 저장
GROUP_WARN_COUNT = {}  # 그룹별 사용자별 경고 횟수 저장
DEFAULT_LIMIT = 3  # 기본 경고한도
GROUP_CHAT_STATS = {}# 그룹별 사용자별 채팅 및 미디어 수 저장을 위한 딕셔너리

def update_chat_stats(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    # 각 사용자의 채팅 수 및 미디어 수를 업데이트
    if user_id not in GROUP_CHAT_STATS:
        GROUP_CHAT_STATS[user_id] = {'text_count': 0, 'media_count': 0}

    if update.message.text:
        GROUP_CHAT_STATS[user_id]['text_count'] += 1
    elif update.message.photo or update.message.document or update.message.audio:
        GROUP_CHAT_STATS[user_id]['media_count'] += 1



def user_info(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        update.message.reply_text('사용자명을 입력해주세요. 예: /info 사용자명')
        return

    target_user_name = args[0]
    target_user_id = None

    for member in context.bot.get_chat(update.message.chat_id).get_members():
        if member.user.username == target_user_name:
            target_user_id = member.user.id
            break

    if target_user_id is None:
        update.message.reply_text(f'사용자 {target_user_name}을 찾을 수 없습니다.')
        return

    if target_user_id in GROUP_CHAT_STATS:
        text_count = GROUP_CHAT_STATS[target_user_id]['text_count']
        media_count = GROUP_CHAT_STATS[target_user_id]['media_count']
        user_first_name = member.user.first_name  # 사용자의 실제 이름 가져오기
        update.message.reply_text(f'{user_first_name}님의 채팅 수: {text_count}개, 미디어 수: {media_count}개')
    else:
        update.message.reply_text(f'{user_first_name}님은 아직 채팅을 보내지 않았습니다.')
        

def set_group_limit(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    user_status = context.bot.get_chat_member(chat_id, user_id).status

    if user_status == 'administrator' or user_status == 'creator':
        try:
            limit = int(context.args[0])
            GROUP_LIMITS[chat_id] = limit
            update.message.reply_text(f'그룹의 경고한도가 {limit}로 설정되었습니다.')
        except (IndexError, ValueError):
            update.message.reply_text('올바른 형식으로 그룹의 경고한도를 설정해주세요.\n예: /limit 3')
    else:
        update.message.reply_text('그룹 관리자만 사용 할 수 있는 기능입니다.')


def ban_user(update: Update, user_id, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.kick_chat_member(chat_id, user_id)
    update.message.reply_text('사용자가 밴 처리되었습니다.')
    
def unban_user(update: Update, user_id, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.unban_chat_member(chat_id, user_id)
    update.message.reply_text('사용자의 밴이 해제되었습니다.')


def reduce_warn(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_status = context.bot.get_chat_member(update.message.chat_id, user_id).status
    if user_status == 'administrator' or user_status == 'creator':
        args = context.args
        if not args or len(args) < 2:
            update.message.reply_text('올바른 형식으로 사용해주세요.\n예: /reduce_warn 사용자명 감소할 경고 수')
            return

        target_user_name = args[0]
        try:
            reduce_count = int(args[1])
        except ValueError:
            update.message.reply_text('경고 수는 정수로 입력해주세요.')
            return

        for member in context.bot.get_chat(update.message.chat_id).get_members():
            if member.user.username == target_user_name:
                target_user_id = member.user.id
                if target_user_id in GROUP_WARN_COUNT:
                    GROUP_WARN_COUNT[target_user_id] = max(0, GROUP_WARN_COUNT.get(target_user_id, 0) - reduce_count)
                    current_warn_count = GROUP_WARN_COUNT[target_user_id]
                    group_limit = GROUP_LIMITS.get(update.message.chat_id, DEFAULT_LIMIT)
                    update.message.reply_text(
                        f'{target_user_name}님의 경고 {reduce_count}개를 감소했습니다.\n현재 경고: {current_warn_count}/{group_limit}'
                    )
                else:
                    update.message.reply_text(f'{target_user_name}님은 경고를 받은 적이 없습니다.')
                return

        update.message.reply_text(f'사용자 {target_user_name}을 찾을 수 없습니다.')
    else:
        update.message.reply_text('그룹 관리자만 사용 할 수 있는 기능입니다.')


def warn(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_status = context.bot.get_chat_member(update.message.chat_id, user_id).status
    if user_status == 'administrator' or user_status == 'creator':
        args = context.args
        if not args or len(args) < 2:
            update.message.reply_text('올바른 형식으로 사용해주세요.\n예: /warn 사용자명 추가할_경고_수')
            return

        target_user_name = args[0]
        try:
            warn_count = int(args[1])
        except ValueError:
            update.message.reply_text('경고 수는 정수로 입력해주세요.')
            return

        for member in context.bot.get_chat(update.message.chat_id).get_members():
            if member.user.username == target_user_name:
                target_user_id = member.user.id
                if target_user_id in GROUP_WARN_COUNT:
                    GROUP_WARN_COUNT[target_user_id] = GROUP_WARN_COUNT.get(target_user_id, 0) + warn_count
                    current_warn_count = GROUP_WARN_COUNT[target_user_id]
                    group_limit = GROUP_LIMITS.get(update.message.chat_id, DEFAULT_LIMIT)
                    update.message.reply_text(
                        f'{target_user_name}님에게 경고 {warn_count}개를 추가했습니다.\n현재 경고: {current_warn_count}/{group_limit}'
                    )
                    if current_warn_count >= group_limit:
                        ban_user(update, target_user_id)  # 경고 한도 초과 시 사용자 밴 처리
                        update.message.reply_text('사용자가 밴 처리되었습니다.')
                else:
                    GROUP_WARN_COUNT[target_user_id] = warn_count
                    update.message.reply_text(
                        f'{target_user_name}님에게 경고 {warn_count}개를 추가했습니다.\n현재 경고: {warn_count}'
                    )
                return

        update.message.reply_text(f'사용자 {target_user_name}을 찾을 수 없습니다.')
    else:
        update.message.reply_text('그룹 관리자만 사용 할 수 있는 기능입니다.')

# def message_handler(update: Update, context: CallbackContext):
    #chat_id = update.message.chat_id
    #user_id = update.message.from_user.id
    #user_name = update.message.from_user.username
    #text = update.message.text.lower()

    #if chat_id in GROUP_LIMITS and user_id not in LIMITS:
        #if text.endswith('노') and not text.startswith('야노'):
            #GROUP_WARN_COUNT[user_id] = GROUP_WARN_COUNT.get(user_id, 0) + 1
            #if GROUP_WARN_COUNT[user_id] >= GROUP_LIMITS[chat_id]:
                #ban_user(update, user_id)  # 경고 한도 초과 시 사용자 밴 처리

            #update.message.reply_text(
                #f'{user_name}님에게 경고를 1 추가했습니다. 현재 경고: {GROUP_WARN_COUNT.get(user_id, 0)}'
            #)

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(token=TOKEN, use_context=True, request_kwargs={'read_timeout': 6, 'connect_timeout': 7})
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text | Filters.photo | Filters.document | Filters.audio, update_chat_stats))
    dp.add_handler(CommandHandler('info', user_info, pass_args=True))
    dp.add_handler(CommandHandler('set_limit', set_group_limit, pass_args=True))
    dp.add_handler(CommandHandler('ban', ban_user, pass_args=True))
    dp.add_handler(CommandHandler('unban', unban_user, pass_args=True))
    dp.add_handler(CommandHandler('warn', warn, pass_args=True))
    dp.add_handler(CommandHandler('reduce_warn', reduce_warn, pass_args=True))
    #dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()




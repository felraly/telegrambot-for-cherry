from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# �ڷ��׷� ���� ��ū�� �Է��ϼ���
TOKEN = '6321575706:AAFdH-lVl5r3Ai0DhFlQHsyt_mK0dpakMnc'

def start(update, context):
    update.message.reply_text('�ȳ��ϼ���! /warn�� �Է��ϸ� "��" ���� �޽����� ��� ��µ˴ϴ�.')

def warn(update, context):
    update.message.reply_text('���: "��" ���� �޽����� �����Ǿ����ϴ�!')

def message_handler(update, context):
    text = update.message.text.lower()
    if text.endswith('��'):
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

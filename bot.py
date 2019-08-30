import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton
from telegram.ext import Updater, MessageHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
from equation_solver import Solve_Square_Eq

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Приветствие"""
    update.message.reply_text(
        'Привет, я бот, который очень любит решать квадратные уравнения:3\nНапиши мне /cat и я поделюсь ими с тобой')


def help(bot, update):
    """Сообщение для помощи с командами"""
    update.message.reply_text('Чтобы получить решение напиши сообщение вида: \solve A,B,C (Ах2 + Вх + С = 0)')


def echo(bot, update):
    """На любой текст отвечаем ошибкой"""
    update.message.reply_text("Неизвестная команда :(")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def send_solution(bot, update, user_data):
    '''Send solution link'''
    msg = update.message.text
    if msg.startswith('eq:'):
        # a, b, c = tuple(map(int, msg.split(':')[1].split))
        a, b, c = 2, 3, 4
        # link = Solve_Square_Eq(aa=a, bb=b, cc=c)
        link = '2'
        resp_text = '{}x2{:+}x{:+}=0 solution: {}'.format(a, b, c, link)
        update.message.reply_text = resp_text
    else:
        update.message.reply_text = 'Формат сообщения: \'eq: A B C\' '
    # bot.send_message(chat_id=update.message.chat_id, text=resp_text)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("909581341:AAGeuFjGcOxkLzzCg2gqv0O5JELN1Fg8a1s")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # dp.add_handler(CallbackQueryHandler(get_callback_from_button))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    # dp.add_handler(CommandHandler("cat", sendcat))
    dp.add_handler(MessageHandler(Filters.text, send_solution, pass_user_data=True) )

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

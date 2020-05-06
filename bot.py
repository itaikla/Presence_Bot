from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from itertools import chain
import logging
import telegram

TOKEN = "X"

SUMMARY = "Summary"
GOING = "On the way"
SICK_LEAVE = "Sick leave"
VACATION = "Vacation"
ON_DUTY_OUTSIDE = "On duty outside"
STUDY = "Study"
LATING = "Lating"

OPTIONS = [[GOING], [VACATION, ON_DUTY_OUTSIDE, SICK_LEAVE], [STUDY, LATING], [SUMMARY]]
statuses = {}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def print_status_summary(update, context):
    if statuses:
        summary_format = ""
        for person, status in statuses.items():
            summary_format += "{0} - {1}".format(person, status)
            summary_format += '\n'
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=summary_format)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="No reports yet today")


def start(update, context):
    options_keyboard = telegram.ReplyKeyboardMarkup(keyboard=OPTIONS)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Good morning, choose your status please!",
                             reply_markup=options_keyboard)


def on_receiving_message(update, context):
    if not update.message.from_user.is_bot:
        message_status = update.message.text
        if message_status == SUMMARY:
            print_status_summary(update, context)
        elif message_status in chain(*OPTIONS):
            user = "{0} {1} ({2})".format(update.message.from_user.first_name,
                                          update.message.from_user.last_name,
                                          update.message.from_user.username)
            if message_status == GOING:
                pass
            # Add <user: status> to the dictionary
            statuses.update({user: message_status})
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Thank You!")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Try Another Status!")


if __name__ == '__main__':

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(Filters.text, on_receiving_message)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)

    updater.start_polling()

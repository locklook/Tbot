from telegram import Bot
from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ParseMode
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import Filters


TOKEN = "1343619920:AAEgiEvmEWnvtOXKLKN_uVHHaQLfuXBxE9c"

BUTTON_1 = "button_1"
BUTTON_2 = "button_2"

TITLES = {
    BUTTON_1 : "Кнопка 1",
    BUTTON_2 : "Кнопка 2",
}
Key_BUTTON_1 = "Помощь"
Key_BUTTON_2 = "Панель кнопок"
Key_BUTTON_3 = "Убрать панель"

def button_panel():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[BUTTON_1], callback_data=BUTTON_1),
            InlineKeyboardButton(TITLES[BUTTON_2], callback_data=BUTTON_2),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
def button_handler(bot: Bot,update: Update, chat_data=None, **kwargs):
    query = update.callback_query
    data = query.data

    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text

    if data == BUTTON_1:
        query.edit_message_text(
            text=current_text,
            parse_mode=ParseMode.MARKDOWN,
        )
        bot.send_message(
            chat_id=chat_id,
            text='Вы нажали на "Кнопку 1"',
        )
    elif data == BUTTON_2:
        query.edit_message_text(
            text="Вы нажали на кнопку 2",
            reply_markup=button_panel()
        )

def button_keyboard():
    keyboard = [
        [
            KeyboardButton(Key_BUTTON_1),
            KeyboardButton(Key_BUTTON_2),
        ],
        [
            KeyboardButton(Key_BUTTON_3)
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )

def do_start(bot: Bot,update: Update):

    bot.send_message(
         chat_id=update.message.chat_id,
         text="Привет!",
         reply_markup=button_keyboard()
    )

def do_help(bot: Bot,update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Я тестовый бот, пока что у меня нету функцый",
)

def do_panel(bot: Bot,update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Панель кнопок:",
        reply_markup=button_panel(),
    )

def do_echo(bot: Bot,update: Update):
    chat_id = update.message.chat_id
    text = update.message.text
    if text == Key_BUTTON_1:
        return do_help(bot=bot, update=update)
    elif text == Key_BUTTON_2:
        return do_panel(bot=bot, update=update)
    elif text == Key_BUTTON_3:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Вы убрали панель",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Команда неверная",
        )


def main():
    bot = Bot(
        token=TOKEN,
    )
    updater = Updater(
        bot=bot,
    )



    start_handler = CommandHandler("start", do_start)
    help_handler = CommandHandler("help", do_help)
    button_panel_handler = CommandHandler("panel", do_panel)
    message_handler = MessageHandler(Filters.text, do_echo)
    button_event = CallbackQueryHandler(callback=button_handler, pass_chat_data=True)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(button_panel_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(button_event)


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

from telegram import ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random
import os

updater = Updater('1859480870:AAGlwGe-zEu2St5nEUqGOFuYbLmU6HR3Bkw')


def start(update, _: CallbackContext):

    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"Привет, {user.mention_markdown_v2()}\!" + "\n Я знаю следующие команды: "
                                                     "\n/start начинаю работу"
                                                     "\n/help рассказываю о возможностях"
                                                     "\n/picture отправляю картинку",
        reply_markup=ForceReply(selective=False)
    )


def command_help(update, _: CallbackContext):

    update.message.reply_text(
        "Я знаю следующие команды: "
        "\n/start начинаю работу"
        "\n/help рассказываю о возможностях"
        "\n/picture отправляю картинку"
        "\nКроме того, я могу отпралять картинки по просьбе 'Отправь кота'")


def echo(update, _: CallbackContext):

    if "?" in update.message.text:

        update.message.reply_text('По совету моего адвоката, я не буду отвечать на этот вопрос')

    elif " я " in update.message.text:

        update.message.reply_text(fr'Нет, {update.message.text}')

    else:

        update.message.reply_text(fr'{update.message.text}')


def send_picture(update, context):

    files = os.listdir('images')
    image = random.choice(files)
    photo = open('images\\' + image, 'rb')

    chat_id = update.message.chat_id

    context.bot.send_photo(chat_id=chat_id, photo=photo)


def main():

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", command_help))
    dispatcher.add_handler(CommandHandler("picture", send_picture))
    dispatcher.add_handler(MessageHandler(Filters.text({"Отправь кота",
                                                        "Скинь кота",
                                                        "Покажи кота"}), send_picture))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()

    updater.idle()


main()

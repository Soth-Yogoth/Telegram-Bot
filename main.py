from telegram import ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from recognize import *
import random
import os

updater = Updater('1859480870:AAHk-CcpYem1eeJpT3ZhJWZ2QLqUDFUF9IQ')


def start(update, _: CallbackContext):

    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"Привет, {user.mention_markdown_v2()}\!" + "\n Я знаю следующие команды: "
                                                     "\n/start начинаю работу"
                                                     "\n/help рассказываю о своих возможностях"
                                                     "\n/picture отправляю картинку"
                                                     "\n/joke рассказываю шутку",
        reply_markup=ForceReply(selective=False)
    )


def command_help(update, _: CallbackContext):

    update.message.reply_text(
        "Я знаю следующие команды: "
        "\n/start начинаю работу"
        "\n/help рассказываю о возможностях"
        "\n/picture отправляю картинку"
        "\n/joke рассказываю шутку"
        "\n\nА ещё я умею отпралять картинки и шутить по просьбам 'Отправь кота' и 'Пошути'."
        "\n\nКроме того, могу попытаться угадать породу кота по фотографии. "
        " К сожалению, пока что я знаю всего 5 пород: абиссинская, "
        "бенгальская, бирманская, бомбейская и британская короткошерстная.")


def echo(update, _: CallbackContext):

    if "?" in update.message.text:

        update.message.reply_text('По совету моего адвоката, я не буду отвечать на этот вопрос')

    elif " я " in update.message.text:

        update.message.reply_text(fr'Нет, {update.message.text}')

    else:

        update.message.reply_text(fr'{update.message.text}')


def tell_joke(update, _: CallbackContext):

    jokes = ["Говорят, что кошки и дрессировка несовместимы. Это неправда. Мой кот выдрессировал меня за два дня",
             "Забыл вчера кота покормить. Утром просыпаюсь, чем-то гремит на кухне. Наверное, готовит",
             "По стенам не лазь... Когти о диван не точи... Хорошо хоть рыбок в аквариуме не пересчитывают",
             "Сегодня отключили интернет на целый день. И знаете, что я заметил? Коты не моргают",
             "Если в Москве черная кошка перебежала дорогу, значит, ей крупно повезло",
             "По выходным добрая фея превращает меня в кота — я много ем, сплю и болтаюсь по квартире, ничего не делая"]

    joke = random.choice(jokes)
    update.message.reply_text(joke)


def send_picture(update, context):

    files = os.listdir('images')
    image = random.choice(files)
    photo = open('images\\' + image, 'rb')

    chat_id = update.message.chat_id

    context.bot.send_photo(chat_id=chat_id, photo=photo)


def recognize_picture(update, _: CallbackContext):

    update.message.reply_text("Хмм, дай-ка подумать...")

    image = update.message.photo[0].get_file()
    prediction, probabilities = recognizing(image)

    result = ("Это похоже на кошку породы " + str(prediction[0])
              + ' я уверен в этом на ' + "%.0f" % probabilities[0] + '%')
    update.message.reply_text(result)

    result2 = ("Хотя с вероятностью " + "%.0f" % probabilities[1] + '%'
               + ' это всё-таки ' + str(prediction[1]))
    update.message.reply_text(result2)


def main():

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", command_help))
    dispatcher.add_handler(CommandHandler("picture", send_picture))
    dispatcher.add_handler(CommandHandler("joke", tell_joke))

    dispatcher.add_handler(MessageHandler(Filters.text({"Отправь кота",
                                                        "Скинь кота",
                                                        "Покажи кота"}), send_picture))
    dispatcher.add_handler(MessageHandler(Filters.text({"Пошути",
                                                        "Расскажи шутку"}), tell_joke))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_handler(MessageHandler(Filters.photo, recognize_picture))
    updater.start_polling()

    updater.idle()


main()

from telegram import ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from imageai.Classification.Custom import CustomImageClassification
import random
import os

updater = Updater('1859480870:AAGlwGe-zEu2St5nEUqGOFuYbLmU6HR3Bkw')


def start(update, _: CallbackContext):

    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"Привет, {user.mention_markdown_v2()}\!" + "\n Я знаю следующие команды: "
                                                     "\n/start начну работу"
                                                     "\n/help расскажу о своих возможностях"
                                                     "\n/picture отправлю картинку",
        reply_markup=ForceReply(selective=False)
    )


def command_help(update, _: CallbackContext):

    update.message.reply_text(
        "Я знаю следующие команды: "
        "\n/start начинаю работу"
        "\n/help рассказываю о возможностях"
        "\n/picture отправляю картинку"
        "\n\nА ещё я умею отпралять картинки по просьбе 'Отправь кота'."
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


def send_picture(update, context):

    files = os.listdir('images')
    image = random.choice(files)
    photo = open('images\\' + image, 'rb')

    chat_id = update.message.chat_id

    context.bot.send_photo(chat_id=chat_id, photo=photo)


def recognize_picture(update, _: CallbackContext):

    update.message.reply_text("Хмм, дай-ка подумать...")

    image = update.message.photo[0].get_file()
    image.download('user_photo.jpg')
    model = "model_ex-010_acc-0.836387.h5"

    execution_path = os.getcwd()

    prediction = CustomImageClassification()
    prediction.setModelTypeAsInceptionV3()
    prediction.setModelPath(os.path.join(execution_path, model))
    prediction.setJsonPath(os.path.join(execution_path, "model_class.json"))
    prediction.loadModel(num_objects=5)

    prediction, probabilities = prediction.classifyImage('user_photo.jpg', result_count=2)

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
    dispatcher.add_handler(MessageHandler(Filters.text({"Отправь кота",
                                                        "Скинь кота",
                                                        "Покажи кота"}), send_picture))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_handler(MessageHandler(Filters.photo, recognize_picture))
    updater.start_polling()

    updater.idle()


main()

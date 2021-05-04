import telebot
from flask import Flask, request
import os

TOKEN = "1799537586:AAHHctNYx3h8m4-1ezE0NtrFyskczL91irs"
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)

def findat(msg):
    # from a list of texts, it finds the one with the '@' sign
    for i in msg:
        if '@' in i:
            return i

@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    bot.reply_to(message, "欢迎来到Leyao的Rogers/Fido自动机器人！\nWelcome to Leyao's Rogers/Fido BOT!")

@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):
    bot.reply_to(message, '这个机器人将帮助客户选择需要的套餐和下单。\nThis BOT will help our customer to find the best plan for them and place the order.')

@bot.message_handler(func=lambda msg: msg.text is not None and '@' in msg.text)
# lambda function finds messages with the '@' sign in them
# in case msg.text doesn't exist, the handler doesn't process it
def at_converter(message):
    texts = message.text.split()
    at_text = findat(texts)
    if at_text == '@': # in case it's just the '@', skip
        pass
    else:
        insta_link = "https://instagram.com/{}".format(at_text[1:])
        bot.reply_to(message, insta_link)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://hidden-dusk-82997.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
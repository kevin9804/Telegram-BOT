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
    bot.send_message(message.chat.id, "欢迎来到Leyao的Rogers/Fido自动机器人！\n"
    +"Welcome to Leyao's Rogers/Fido BOT!\n"
    +"请使用/help 指令了解如何使用此机器人\n"
    +"Please use /help command to learn more about how to use this BOT", disable_web_page_preview=True, parse_mode='Markdown')

@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):
    bot.send_message(message.chat.id, '这个机器人将帮助客户选择需要的套餐和下单。\n'
    +'This BOT will help our customer to find the best plan for them and place the order.\n'
    +'使用以下命令选择您想了解的套餐\n'
    +'Use the following command to learn the package\n'
    +'/fido_wireless\n/fido_home_internet\n/rogers_wireless\n'
    +'/rogers_home_internet\n/virgin_home_internet\n/bell_home_internet\n'
    +'/ctexcel\n/cmlink', parse_mode='Markdown')

@bot.message_handler(commands=['fido_wireless']) # fido wireless message handler
def send_welcome(message):
    bot.send_message(message.chat.id, '这里是FIDO的手机套餐。\n'
    +'Here is the fido wireless plan', parse_mode='Markdown')


# @bot.message_handler(func=lambda msg: msg.text is not None and '@' in msg.text)
# lambda function finds messages with the '@' sign in them
# in case msg.text doesn't exist, the handler doesn't process it
# def at_converter(message):
#    texts = message.text.split()
#    at_text = findat(texts)
#    if at_text == '@': # in case it's just the '@', skip
#        pass
#    else:
#        insta_link = "https://instagram.com/{}".format(at_text[1:])
#        bot.send_message(message.chat.id, insta_link)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://leyao-telegram-bot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
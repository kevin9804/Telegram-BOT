import telebot
from flask import Flask, request
from telebot import types
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
def send_help(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    itembtn1 = types.InlineKeyboardButton('FIDO', url='www.fido.ca')
    itembtn2 = types.InlineKeyboardButton('ROGERS', url='www.rogers.com')
    itembtn3 = types.InlineKeyboardButton('CTEXCEL', url='www.ctexcel.ca')
    itembtn4 = types.InlineKeyboardButton('CMLINK', url='http://cmlink.com/ca/zh')
    markup.row(itembtn1, itembtn2)
    markup.row(itembtn3, itembtn4)
    bot.send_message(message.chat.id, '这个机器人将帮助客户选择需要的套餐和下单。\n'
    +'This BOT will help our customer to find the best plan for them and place the order.\n'
    +'使用以下命令选择您想了解的套餐\n'
    +'Use the following command to learn the package\n'
    +'/fido_wireless\n/fido_home_internet\n/rogers_wireless\n'
    +'/rogers_home_internet\n/virgin_home_internet\n/bell_home_internet\n'
    +'/ctexcel\n/cmlink', reply_markup=markup)

@bot.message_handler(commands=['fido_wireless']) # fido wireless message handler
def send_fido(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('Ottawa')
    btn2 = types.KeyboardButton('National (non Ottawa/Quebec)')
    btn3 = types.KeyboardButton('Quebec')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.char.id, 'Please select the area of your number area code:', reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text is not None and 'Ottawa' in msg.text)
    photo = open('info/fido/wireless/OTT_rate.jpg','rb')
    bot.send_photo(message.chat.id, photo, caption='Here is the price plan for Ottawa Numbers')

@bot.message_handler(commands=['fido_home_internet']) # fido wireless message handler
def send_fido(message):
    bot.send_message(message.chat.id, '图中为FIDO家庭网络套餐\nThere are fido home internet plan in the pictures')

# Handle all undefined messages
@bot.message_handler(content_types=['text'])
def default_command(message):
    bot.send_message(message.chat.id, "我还在学习中，暂时不知道如何回复您哦！\nHi, I am still learning how to reply this message at this moment.")

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
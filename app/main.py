import telebot
from telebot import types
from fastapi import FastAPI
import threading

# FastAPI app
app = FastAPI()

# Replace with your actual API Token
BOT_TOKEN = '7013617002:AAF7_od3vC5a-KOGCXAmjE-5Tup87wEj14c'

bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary to keep track of user states and check clicks
user_states = {}

# Define airdrop details (unique name, link, and instructions for each button)
airdrops = {
    1: {"name": "Abstract Chain Testnet", "link": "https://abstract.deform.cc/?referral=WlP2bFqxLMmj", "instructions": "https://t.me/crepto_mining_news/102"},
    2: {"name": "Bless Network", "link": "https://bless.network/dashboard?ref=WBEYNS", "instructions": "https://youtube.com/shorts/uQ8h18klTA0?si=G3bqOkFAcJeBPoXl"},
    # Add other airdrops as required...
}

# Define the different states
WAITING_FOR_AIRDROP_LIST = 'waiting_for_airdrop_list'
WAITING_FOR_FIRST_CHECK = 'waiting_for_first_check'
WAITING_FOR_SECOND_CHECK = 'waiting_for_second_check'
WAITING_FOR_GET_LIST = 'waiting_for_get_list'

# Define the "Get Airdrop List" logic
def handle_get_airdrop_list(message):
    user_states[message.chat.id] = WAITING_FOR_FIRST_CHECK
    channel_url = 'https://t.me/crepto_mining'
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Join our channel', url=channel_url))
    markup.add(types.InlineKeyboardButton('Check', callback_data='check'))
    bot.send_message(message.chat.id, 'Join our channel to access the airdrop list.', reply_markup=markup)

# Define the first check logic
def handle_first_check(message):
    bot.send_message(message.chat.id, "Subscribe to the channel and click 'Check' again.")
    user_states[message.chat.id] = WAITING_FOR_SECOND_CHECK
    markup = types.InlineKeyboardMarkup()
    channel_url = 'https://t.me/crepto_mining'
    markup.add(types.InlineKeyboardButton('Join our channel', url=channel_url))
    markup.add(types.InlineKeyboardButton('Check', callback_data='check'))
    bot.send_message(message.chat.id, 'Click "Check" after subscribing.', reply_markup=markup)

# Define the second check logic
def handle_second_check(message):
    user_states[message.chat.id] = WAITING_FOR_GET_LIST
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Get List', callback_data='get_list'))
    bot.send_message(message.chat.id, 'You can now access the airdrop list.', reply_markup=markup)

# Define the logic for displaying the airdrop list
def handle_get_list(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i, details in airdrops.items():
        markup.add(
            types.InlineKeyboardButton(details["name"], url=details["link"]),
            types.InlineKeyboardButton("Instructions", url=details["instructions"])
        )
    bot.send_message(message.chat.id, 'Here is your airdrop list:', reply_markup=markup)

# Handle '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_states[message.chat.id] = WAITING_FOR_AIRDROP_LIST
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Get Airdrop List', callback_data='get_airdrop_list'))
    bot.send_message(message.chat.id, "Welcome! Click 'Get Airdrop List' to start.", reply_markup=markup)

# Handle button clicks
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.message.chat.id
    if call.data == 'get_airdrop_list':
        handle_get_airdrop_list(call.message)
    elif call.data == 'check':
        current_state = user_states.get(user_id)
        if current_state == WAITING_FOR_FIRST_CHECK:
            handle_first_check(call.message)
        elif current_state == WAITING_FOR_SECOND_CHECK:
            handle_second_check(call.message)
        elif current_state == WAITING_FOR_GET_LIST:
            bot.send_message(user_id, 'You already completed the actions.')
        else:
            bot.send_message(user_id, 'Unknown state.')
    elif call.data == 'get_list':
        handle_get_list(call.message)
    else:
        bot.send_message(user_id, "Unknown action.")

# Background task for Telebot
def start_telebot():
    bot.polling()

# Start Telebot in a separate thread
threading.Thread(target=start_telebot, daemon=True).start()

# FastAPI endpoint for health check
@app.get("/")
def read_root():
    return {"message": "FastAPI is running with Telebot integration"}

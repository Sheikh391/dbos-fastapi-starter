import telebot
from telebot import types

# Replace with your actual API Token
BOT_TOKEN = '7013617002:AAF7_od3vC5a-KOGCXAmjE-5Tup87wEj14c'

bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary to keep track of user states and check clicks
user_states = {}

# Define airdrop details (unique name, link, and instructions for each button)
airdrops = {
    1: {"name": "Abstract Chain Testnet", "link": "https://abstract.deform.cc/?referral=WlP2bFqxLMmj", "instructions": "https://t.me/crepto_mining_news/102"},
    2: {"name": "Bless Network", "link": "https://bless.network/dashboard?ref=WBEYNS", "instructions": "https://youtube.com/shorts/uQ8h18klTA0?si=G3bqOkFAcJeBPoXl"},
    3: {"name": "Nodepay", "link": "https://app.nodepay.ai/register?ref=qutLumM3bzN3XLB", "instructions": "https://t.me/crepto_mining_guides/574"},
    4: {"name": "Gradient Network", "link": "https://app.gradient.network/signup?code=Y65HAK", "instructions": "https://t.me/crepto_mining_news/69"},
    5: {"name": "Grass", "link": "https://app.getgrass.io/register/?referralCode=7XtNWDYksdry3Jg", "instructions": "https://youtu.be/cbLVdogmuno?si=9k_VLnnwbXgeDbno"},
    6: {"name": "MoonWalk", "link": "https://app.moonwalk.fit/?referral=s3ykh1vx", "instructions": "https://t.me/crepto_mining_news/62"},
    7: {"name": "Sonic Labs", "link": "https://airdrop.soniclabs.com/?ref=e2rveq", "instructions": "https://t.me/crepto_mining_news/59"},
    8: {"name": "Farmroll", "link": "https://farmroll.io/farming/farmroll/quests?ref=C43EADA0C5", "instructions": "https://t.me/crepto_mining_news/55"},
    9: {"name": "Dawn", "link": "https://chromewebstore.google.com/detail/dawn-validator-chrome-ext/fpdkjdnhkakefebpekbdhillbhonfjjp", "instructions": "https://t.me/crepto_mining_news/53"},
    10: {"name": "Node Mining Trick", "link": "https://youtu.be/BI4pExSHtjc?si=bx3Na3JVbjgZUjuQ", "instructions": "https://youtu.be/BI4pExSHtjc?si=bx3Na3JVbjgZUjuQ"}
}

# Define the different states
WAITING_FOR_AIRDROP_LIST = 'waiting_for_airdrop_list'
WAITING_FOR_FIRST_CHECK = 'waiting_for_first_check'
WAITING_FOR_SECOND_CHECK = 'waiting_for_second_check'
WAITING_FOR_GET_LIST = 'waiting_for_get_list'

# Define the "Get Airdrop List" logic
def handle_get_airdrop_list(message):
    # Store the user state
    user_states[message.chat.id] = WAITING_FOR_FIRST_CHECK

    # Send a message with instructions and URL button
    channel_url = 'https://t.me/crepto_mining'  # Replace with your actual channel URL
    button_text = 'Join our channel'
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(button_text, url=channel_url))
    markup.add(types.InlineKeyboardButton('Check', callback_data='check'))
    bot.send_message(message.chat.id, 'To access the airdrop list, you need to join our telegram channel.', reply_markup=markup)

# Define the first check logic
def handle_first_check(message):
    # Inform the user to subscribe
    bot.send_message(message.chat.id, "Looks like you haven't joined our channel yet. Kindly subscribe to our channel.")

    # Update the user state
    user_states[message.chat.id] = WAITING_FOR_SECOND_CHECK

    # Add a URL button and "Check" button
    markup = types.InlineKeyboardMarkup()
    channel_url = 'https://t.me/crepto_mining'  # Replace with your actual channel URL
    markup.add(types.InlineKeyboardButton('Join our channel', url=channel_url))
    markup.add(types.InlineKeyboardButton('Check', callback_data='check'))
    bot.send_message(message.chat.id, 'Click "Check" again after subscribing.', reply_markup=markup)

# Define the second check logic
def handle_second_check(message):
    # Update the user state
    user_states[message.chat.id] = WAITING_FOR_GET_LIST

    # Send a message confirming that the user can now get the list
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Get List', callback_data='get_list'))
    bot.send_message(message.chat.id, 'You have completed the steps! 🎉 Click "Get List" to view the airdrops.', reply_markup=markup)

# Define the logic for displaying the airdrop list with an "Instructions" button
def handle_get_list(message):
    # Send a message with the list of airdrops as buttons
    markup = types.InlineKeyboardMarkup(row_width=2)  # Allow two buttons per row
    for i, details in airdrops.items():  # Loop through all airdrops
        # Add the airdrop button and its "Instructions" button side by side
        markup.add(
            types.InlineKeyboardButton(details["name"], url=details["link"]),
            types.InlineKeyboardButton("Instructions", url=details["instructions"])
        )
    bot.send_message(message.chat.id, 'Here is your airdrop list:', reply_markup=markup)

# Create your buttons
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Initialize user state
    user_states[message.chat.id] = WAITING_FOR_AIRDROP_LIST

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Get Airdrop List', callback_data='get_airdrop_list'))
    bot.send_message(message.chat.id, "Welcome! Click 'Get Airdrop List' to start:", reply_markup=markup)

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
            bot.send_message(user_id, 'You have already completed the required actions.')
        else:
            bot.send_message(user_id, 'Unknown state or action.')
    elif call.data == 'get_list':
        handle_get_list(call.message)
    else:
        bot.send_message(user_id, "Unknown action.")

# Start the bot
bot.polling()


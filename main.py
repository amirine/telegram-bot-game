import telebot

import settings
from game_calculations import RPSGame as Game
from players_db import PlayersDataBase as DB

bot = telebot.TeleBot(settings.TOKEN)


@bot.message_handler(content_types=['text'])
def start(message):
    """Game start function"""
    if message.text and not settings.START_GAME_PLAYER_ID and not settings.GAME_OPPONENT_ID:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.row('yes', 'no')
        bot.send_message(message.from_user.id, f'Hi, {message.from_user.first_name}! Welcome to our new PSS game!'
                                               'Would you like to start the game?', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_opponent)


@bot.message_handler(content_types=['text'])
def get_opponent(message):
    """Writes player data to database, opponent choice"""
    if message.text == 'yes':
        settings.START_GAME_PLAYER_ID = message.from_user.id
        if not DB.check_player_in_db(message.from_user.id):
            DB.add_player_to_db(message.from_user.id, message.from_user.first_name)
        bot.send_message(message.from_user.id, 'Nice! Now you can choose your opponent. Just enter the index number.')
        bot.send_message(message.from_user.id, DB.get_all_players(message.from_user.id))
        bot.register_next_step_handler(message, message_for_opponent)
    else:
        bot.send_message(message.from_user.id, 'So... Your choice. Will be glad to see you later!')
        settings.START_GAME_PLAYER_ID = 0
        settings.GAME_OPPONENT_ID = 0
        bot.register_next_step_handler(message, start)


@bot.message_handler(content_types=['text'])
def message_for_opponent(message):
    """Writes opponent to confirm participation"""
    if DB.check_input_for_opponent(message.text):
        settings.GAME_OPPONENT_ID = DB.get_player_telegram_id(int(message.text))
        opponent_name = DB.get_player_name(int(message.text))
        bot.send_message(message.from_user.id, f"Great! We'll write {opponent_name} to confirm participation.")
        keyboard = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
        keyboard.row('yes', 'no')
        message = bot.send_message(settings.GAME_OPPONENT_ID, f"Hi, {opponent_name}. How about playing PSS game with "
                                                              f"{message.from_user.first_name} right now?",
                                   reply_markup=keyboard)
        bot.register_next_step_handler(message, get_opponent_confirmation)
    else:
        bot.send_message(message.from_user.id, f"Sorry, player doesn't exist! Start again.")
        settings.START_GAME_PLAYER_ID = 0
        settings.GAME_OPPONENT_ID = 0
        bot.register_next_step_handler(message, start)


@bot.message_handler(content_types=['text'])
def get_opponent_confirmation(message):
    """Gets opponent confirmation, writes permissible variants for the RPS game to choose"""
    if message.text == 'yes':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
        keyboard.row('stone', 'scissors', 'paper')
        message = bot.send_message(settings.START_GAME_PLAYER_ID, f'Agreed!\nLets go! Your choice?',
                                   reply_markup=keyboard)
        bot.register_next_step_handler(message, get_my_choice)
    else:
        bot.send_message(settings.START_GAME_PLAYER_ID, f'Maybe later :(')
        settings.START_GAME_PLAYER_ID = 0
        settings.GAME_OPPONENT_ID = 0
        bot.register_next_step_handler(message, start)


@bot.message_handler(content_types=['text'])
def get_my_choice(message):
    """Gets start game player choice, requests for the opponent RPS choice"""
    settings.PLAYERS_CHOICES = []
    settings.PLAYERS_CHOICES.append((message.from_user.id, message.from_user.first_name, message.text))
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('stone', 'scissors', 'paper')
    message = bot.send_message(settings.GAME_OPPONENT_ID, 'Your choice?', reply_markup=keyboard)
    bot.register_next_step_handler(message, get_opponent_choice)


@bot.message_handler(content_types=['text'])
def get_opponent_choice(message):
    """Gets opponent RPS choice, prints results to players"""
    settings.PLAYERS_CHOICES.append((message.from_user.id, message.from_user.first_name, message.text))
    bot.send_message(settings.START_GAME_PLAYER_ID, Game.results_print(settings.PLAYERS_CHOICES))
    bot.send_message(settings.GAME_OPPONENT_ID, Game.results_print(settings.PLAYERS_CHOICES))
    keyboard = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
    if not Game.get_winner(settings.PLAYERS_CHOICES)[0]:
        bot.send_message(settings.GAME_OPPONENT_ID, "Draw!", reply_markup=keyboard)
        message = bot.send_message(settings.START_GAME_PLAYER_ID, "Draw!", reply_markup=keyboard)
    else:
        bot.send_message(Game.get_winner(settings.PLAYERS_CHOICES)[0], "Congrats! You're a winner!",
                         reply_markup=keyboard)
        bot.send_message(Game.get_winner(settings.PLAYERS_CHOICES)[1], "Sorry! You've lost!",
                         reply_markup=keyboard)
    settings.START_GAME_PLAYER_ID = 0
    settings.GAME_OPPONENT_ID = 0
    bot.register_next_step_handler(message, start)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

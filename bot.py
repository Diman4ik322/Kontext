from telebot import TeleBot
from telebot.types import Message
from typing import List, Tuple
from model import init, get_placement
init_word, word_dict = init()
similarities = []
 
TOKEN = ''
bot = TeleBot(TOKEN)
print(f"Слово: {init_word}\nСлова: {dict(list(word_dict.items())[:10])}")
 
 
def get_string_words(simiLarities: List[Tuple[str, int]]) -> str:
    end_string = ""
    for sim, count in simiLarities:
        end_string += f"{sim} {count}\n"
    return end_string
@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.username}!\n чтобы играть используй команду /word \
                     \nПример: /word машина")
@bot.message_handler(commands=["word"])
def word(message: Message):
    global similarities, word_dict, init_word
    if len(message.text.split(" ")) > 2:
        bot.send_message(message.chat.id, "Больше одного словап нельзя!")
        return
    _, word = message.text.split(" ")
    if word == init_word:
        bot.send_message(message.chat.id, "Правильно!")
        init_word, word_dict = init()
        similarities = []
        return
    place = get_placement(word,word_dict)
    if place == -1:
        bot.send_message(message.chat.id, "Очень далеко!")
        return
    similarities.append((word,place))
    similarities.sort(key=lambda tup: tup[1])
    msg = get_string_words(similarities)
    bot.send_message(message.chat.id, msg)
 
 
bot.polling(non_stop=True, interval=1)
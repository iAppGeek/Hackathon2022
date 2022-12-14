# install requirements
import initalise

from our_chatbot import chatbot

print("chatbot started")

while True:
    try:
        bot_input = chatbot.get_response(input())
        print(bot_input)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break
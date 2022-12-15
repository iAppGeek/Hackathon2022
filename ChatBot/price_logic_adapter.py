from chatterbot.logic import LogicAdapter
from ric_identifier import identify_ric
import pandas as pd

chat_data = pd.read_csv("test_data.csv")
price_talk = []
for idx in range(len(chat_data.question)):
    price_talk.append([chat_data.question[idx], chat_data.answer[idx]])


class PriceLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        from chatterbot import ChatBot
        from chatterbot.trainers import ListTrainer

        self.inner_chatbot = ChatBot(
            'PriceLogicBot',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri='sqlite:///PriceLogicBot.db',
            read_only=True,
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'maximum_similarity_threshold': 0.20,
                    'default_response': 'NO',
                }
            ]
        )

        list_trainer = ListTrainer(self.inner_chatbot)
        for i in price_talk:
            list_trainer.train(i)

    def can_process(self, statement):
        bot_input = self.inner_chatbot.get_response(statement.text)
        return bot_input.text != "NO" and identify_ric(statement.text)

    def process(self, input_statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement
        import requests

        bot_input = self.inner_chatbot.get_response(input_statement.text)
        ric_identifier_val = identify_ric(input_statement.text).split('.')[0]
        print("Checking the {}".format(bot_input.text))

        if bot_input.text == "PRICE":
            query_url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={}&apikey=SDS2M5T2UV0VO0VQ'.format(
                ric_identifier_val)
            response = requests.get(query_url)
            data = response.json()
            if response.status_code == 200:
                confidence = 1
            else:
                confidence = 0

            price = data['Global Quote']['05. price']
            response_statement = Statement(
                'The current {} for {} is {}'.format(bot_input.text, ric_identifier_val, price))
            response_statement.confidence = confidence
            return response_statement
        elif bot_input.text == "VOL":
            response_statement = Statement('getting {} for {}'.format(bot_input.text, ric_identifier_val))
            response_statement.confidence = 1
            return response_statement
        else:
            response_statement = Statement('Not found')
            response_statement.confidence = 1
            return response_statement

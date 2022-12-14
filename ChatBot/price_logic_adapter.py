from chatterbot.logic import LogicAdapter

price_talk = [['get me the price for', 'PRICE'],
              ['what is the price of', 'PRICE'],
              ['current price of', 'PRICE'],
              ['current price', 'PRICE'],
              ['when was the latest vol for', 'VOL'],
              ['latest vol surface for', 'VOL'],
              ['latest vol timestamp', 'VOL'],
              ['latest vol save', 'VOL']]

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
        return bot_input.text != "NO"

    def process(self, input_statement, additional_response_selection_parameters):
        print('starting process')

        import random
        from chatterbot.conversation import Statement
        import requests

        bot_input = self.inner_chatbot.get_response(input_statement.text)
        print("doing " + bot_input.text)

        response = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo')
        data = response.json()

        # Randomly select a confidence between 0 and 1
        # confidence = random.uniform(0, 1)
        if response.status_code == 200:
            confidence = 1
        else:
            confidence = 0

        price = data['Global Quote']['05. price']
        response_statement = Statement(text='The current temperature is {}'.format(price))
        response_statement.confidence = confidence

        ric = ''

        print(input_statement, additional_response_selection_parameters)

        return response_statement

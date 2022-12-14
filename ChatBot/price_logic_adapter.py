from chatterbot.logic import LogicAdapter

class PriceLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ['get', 'price']
        if all(x in statement.text.split() for x in words):
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        import random
        from chatterbot.conversation import Statement
        import requests

        response = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo')
        data = response.json()

        # Randomly select a confidence between 0 and 1
        # confidence = random.uniform(0, 1)
        if response.status_code == 200:
            confidence = 0.8
        else:
            confidence = 0

        price = data['Global Quote']['05. price']
        response_statement = Statement(text='The current temperature is {}'.format(price))
        response_statement.confidence = confidence

        ric=''

        print(input_statement, additional_response_selection_parameters)

        return response_statement

from chatterbot import ChatBot
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.response_selection import get_most_frequent_response
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new chatbot named Charlie
chatbot = ChatBot(
    'Terminal',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.db',
    read_only=True,

    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],

    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'help',
            'output_text': 'Confluence like to supported functions: chatterbot.rtfd.org'
        },
        {
            'import_path': 'price_logic_adapter.PriceLogicAdapter'
        },
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": LevenshteinDistance,
            "response_selection_method": get_most_frequent_response
        },
        'chatterbot.logic.MathematicalEvaluation'
    ]
)

# corpusTrainer = ChatterBotCorpusTrainer(chatbot)
# corpusTrainer.train(
#     "chatterbot.corpus.english.conversations"
# )

listTrainer = ListTrainer(chatbot)
price_talk = [['get me the price for A', 'its 5'],
              ['what is the price of A', 'its 5'],
              ['current price of A', 'its 5']]

for i in price_talk:
    listTrainer.train(i)

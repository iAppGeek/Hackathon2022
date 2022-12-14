from chatterbot import ChatBot
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.response_selection import get_most_frequent_response
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

import tensorflow as tf

# Create a new chatbot named Charlie
chatbot = ChatBot(
    'chatbot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///chatbot.db',
    read_only=True,

    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],

    logic_adapters=[
        {
            'import_path': 'price_logic_adapter.PriceLogicAdapter'
        },
        {
            'import_path': 'chatterbot.logic.BestMatch',
            "statement_comparison_function": LevenshteinDistance,
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.85
        },
        'chatterbot.logic.MathematicalEvaluation',
    ]
)

corpusTrainer = ChatterBotCorpusTrainer(chatbot)
corpusTrainer.train(
    "chatterbot.corpus.english"
)

listTrainer = ListTrainer(chatbot)
help_response = 'Confluence link to supported functions: chatterbot.rtfd.org'
help_talk = ['help', 'help me', 'what can i ask', 'possible functions', 'what possible functions can you run', 'what can you do']
for i in help_talk:
    listTrainer.train([i, help_response])



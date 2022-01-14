import json
import random
from datetime import datetime
import time
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier, \
    HistGradientBoostingClassifier, IsolationForest, RandomForestRegressor, AdaBoostClassifier, StackingClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

import logging

start_time = datetime.now()


def clean(text):
    clean_text = ''
    for ch in text.lower():
        if ch in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя ':
            clean_text = clean_text + ch
    return clean_text


with open('BOT_CONFIG.json') as f:
    BOT_CONFIG = json.load(f)
del BOT_CONFIG['intents']['price']
print('кол-во интендов:', len(BOT_CONFIG['intents'].keys()))

texts = []
y = []
for intent in BOT_CONFIG['intents'].keys():
    for example in BOT_CONFIG['intents'][intent]['examples']:
        texts.append(example)
        y.append(intent)
print('примеров', len(texts), 'интендов:', len(y))

train_texts, test_texts, y_train, y_test = train_test_split(texts, y, random_state=42, test_size=0.2)

vectorizer = TfidfVectorizer(ngram_range=(1, 7), encoding='utf-8', decode_error='replace', analyzer='char_wb')
# TfidfVectorizer(ngram_range=(1,5), analyzer='char_wb')
# CountVectorizer(ngram_range=(1, 5), analyzer='char_wb')
X_train = vectorizer.fit_transform(train_texts)
X_test = vectorizer.transform(test_texts)

vocab = vectorizer.get_feature_names_out()
print('словарь векторайзера:', len(vocab))

clf = RandomForestClassifier(n_estimators=300, random_state=0, max_features='sqrt').fit(X_train,
                                                                                        y_train)  # LogisticRegression().fit(X_train, y_train)
print(clf.score(X_train, y_train), clf.score(X_test, y_test))


# LogisticRegression: 0.14893617021276595, RandomForestClassifier: 0.19574468085106383


def get_intent_by_model(text):
    return clf.predict(vectorizer.transform([text]))[0]


def bot(input_text):
    intent = get_intent_by_model(input_text)
    return random.choice(BOT_CONFIG['intents'][intent]['responses'])


print('время векторайзера: ', datetime.now() - start_time)

# input_text = ''
# while input_text != 'stop':
#     input_text = input('спроси меня:')
#     if input_text != 'stop':
#         response = bot(input_text)
#         print(response)
#

# mastrobot_example.py
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# function to handle the /start command
def start(update, context):
    update.message.reply_text('Напиши мне!')


# function to handle the /help command
def help(update, context):
    update.message.reply_text('help command received')


# function to handle errors occured in the dispatcher
def error(update, context):
    update.message.reply_text('an error occured')


# function to handle normal text
def text(update, context):
    answer = bot(update.message.text)
    update.message.reply_text(answer)


def main():
    TOKEN = "5074415805:AAEHUB4alF2F3U801BQEZYl_et1qhQkowVY"

    # create the updater, that will automatically create also a dispatcher and a queue to
    # make them dialoge
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    # add an handler for normal text (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text, text))

    # add an handler for errors
    dispatcher.add_error_handler(error)

    # start your shiny new bot
    updater.start_polling()

    # run the bot until Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()

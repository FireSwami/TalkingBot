import random
import nltk

BOT_CONFIG = {
    'intents': {
        'hello': {
            'examples': ['привет!', 'хай!!', 'прив'],
            'responses': ['здравствуйте', 'хэллоу!', 'хей!!1']
        },
        'bye': {
            'examples': ['пока!', 'покеда!!', 'до свиданья'],
            'responses': ['увидимся))', 'до связи', 'Сайонара']
        },
        'howdoyoudo': {
            'examples': ['как дела?', 'как ты?', 'как поживаешь?', 'как самочувствие?'],
            'responses': ['отлично!', 'грущу', 'я робот, у меня нет чувств']
        }
    }
}
def clean(text):
  clean_text = ''
  for ch in text.lower():
    if ch in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
      clean_text = clean_text + ch
  return clean_text

def get_intent(text):
  for intent in BOT_CONFIG['intents'].keys():
    for example in BOT_CONFIG['intents'][intent]['examples']:
      s1 = clean(text)
      s2 = clean(example)
      if nltk.edit_distance(s1, s2) / max(len(s1), len(s2)) < 0.4:
        return intent
  return 'интент не найден'

def bot(input_text):
  intent = get_intent(input_text)
  if intent != 'интент не найден':
    return random.choice(BOT_CONFIG['intents'][intent]['responses'])
  else:
    return 'интент не найден'

  input_text = ''
  while input_text != 'stop':
      input_text = input()
      if input_text != 'stop':
          response = bot(input_text)
          print(response)


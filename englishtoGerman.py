from deep_translator import GoogleTranslator
to_translate = 'Please tell me the name of the person you are interested in'
translated = GoogleTranslator(source='auto', target='de').translate(to_translate)

print(translated)
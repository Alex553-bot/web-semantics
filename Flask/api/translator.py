from mtranslate import translate as Translate
#from googletrans import Translator
def translate(text, dest): 
	return Translate(text, dest)

text = 'hello how are you ? '
print(translate(text, 'en'))
print(translate(text, 'es'))
print(translate(text, 'pt'))
print(translate(text, 'fr'))

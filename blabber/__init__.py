import json

with open(r'./blabber/voices.json') as data:
    supported_voices = json.load(data)

with open(r'./blabber/languages.json') as data:
    supported_languages = json.load(data)

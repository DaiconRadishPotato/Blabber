# __init__.py
#
# Author: Marcos Avila (DaiconV),
#         Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
# Date created: 5/28/2020
# Date last modified: 5/28/2020
# Python Version: 3.8.1
# License: MIT License

import json

with open(r'./blabber/voices.json') as data:
    supported_voices = json.load(data)

with open(r'./blabber/languages.json') as data:
    supported_languages = json.load(data)

with open(r'./blabber/genders.json') as data:
    supported_genders = set(json.load(data))

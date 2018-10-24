import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def who_did_i_want(ow_hero, heroes):
	results = {}
	for hero in heroes:
		results[hero] = fuzz.ratio(ow_hero, hero)
	hero_answer = ""
	highest_ratio = -1
	for hero, ratio in results.items():
		if ratio > highest_ratio:
			hero_answer = hero
			highest_ratio = ratio
	return hero_answer, highest_ratio

# Bullshit to make the REST API happy
headers = {'User-Agent': 'Overwatch User Agent'}

battletag = input("Enter your Battletag (YourBattleTag#1234): ")
battletag = battletag.replace("#", "-")

ow_heroes = ['ana', 'bastion', 'brigitte', 'doomfist', 'dva', 'genji', 'hanzo', 'junkrat', 'lucio', 'mccree', 'mei', 'mercy', 'moira', 'orisa', 'pharah', 'reaper', 'reinhardt', 'roadhog', 'soldier76', 'sombra', 'symmetra', 'tracer', 'torbjorn', 'winston', 'wrecking_ball', 'zarya', 'zenyatta']

character = input("Which character do you want info on? ")
character, ratio = who_did_i_want(character.lower(), ow_heroes)
while(ratio < 75):
	answer = input("Did you want {0}? (y/n) ".format(character))
	if answer.lower()[0] == 'y':
		break
	character = input("Which character do you want info on? ")
	character, ratio = who_did_i_want(character, ow_heroes)

# GET request on the REST API
r = requests.get("https://owapi.net/api/v3/u/{0}/heroes".format(battletag), headers=headers)

data = r.json()

comp_hero_data = data['us']['heroes']['stats']['competitive'][character]['general_stats'].get('solo_kills', 0)
print(comp_hero_data)

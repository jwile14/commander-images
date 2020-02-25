import requests
import time
import wget
import os
import string
import shutil

card_folder = './cards'

if os.path.exists('commanders.zip'):
	os.remove('commanders.zip')

if os.path.isdir(card_folder):
	for f in os.listdir(card_folder):
		os.remove('/'.join([card_folder, f]))
else:
	os.mkdir(card_folder)

searchTerms = ['q=is:commander', 'order=color']
baseUrl =  'https://api.scryfall.com/cards/search?'

url = baseUrl + '&'.join(searchTerms)

cards = []
errorCards = []

print('Getting commanders...')
while True: 
	time.sleep(0.10)
	res = requests.get(url).json()

	for card in res['data']:
		if 'image_uris' in card.keys():
			cards.append({ 'name': card['name'], 'image_url': card['image_uris']['normal']})
		else:
			errorCards.append(card['name'])

	if not res['has_more']:
		break

	url = res['next_page']

print('Downloading images...')
i = 0
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
for card in cards:
    time.sleep(0.10)
    cardname = str(i) + '_' + ''.join(c for c in card['name'] if c in valid_chars) + '.jpg'
    destination = os.path.join(card_folder, cardname)
    wget.download(card['image_url'], out=destination)
    i += 1

shutil.make_archive('commanders', 'zip', card_folder)
print('\nDone!')
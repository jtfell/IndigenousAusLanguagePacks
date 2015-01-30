###################################################################################################
#
# This script downloads the indiginous language dictionaries from http://ausil.org/ and matches
# each word to its english translation and uses that frequency (if it's available). This isn't the 
# ideal strategy but works when there is no text to run frequency analysis on. The outputted file
# can be run through the java "MakeDict" utility to generate a binary dictionary which can be used
# in a language pack for "AnySoftKeyboard" for Android.
#
# Author: Julian Fell (julian.fell@uq.net.au)
#
###################################################################################################

from BeautifulSoup import BeautifulSoup
import re
import requests

# Language names to download
languageList = ["Burarra", "Bilinarra", 
				"Djinang", "Gurindji", 
				"Iwaidja", "Kriol", 
				"Maung", "Tiwi", 
				"Walmajarri", "Warlpiri"]

# Frequency to attach to words without direct english translation
BASE_FREQ = 75

#
# Downloads the language from the AUSIL website and builds a python dict
# with the structure:  {engWord => indigWord}
#
def buildEnglishToIndiginousDictionary(language):
	DICT = {}

	for i in xrange(26):
		if i < 10:
			url = "http://ausil.org/Dictionary/{0}/index-english/0{1}.htm".format(language, i)
		else:
			url = "http://ausil.org/Dictionary/{0}/index-english/{1}.htm".format(language, i)

		try:
			html = requests.get(url).text
		except:
			print "Could not find dictionary for " + language
			return -1

		soup = BeautifulSoup(html)

		for row in soup.findAll('tr'):
			eng = row.find("span", "lpIndexEnglish")
			indig = row.find("span", "lpLexEntryName")

			if eng and indig:
				DICT[eng.text] = [indig.text]
				lastEng = eng.text
			elif indig:
				otherIndig = DICT[lastEng]
				DICT[lastEng] = [indig.text] + otherIndig
	return DICT


# Do the whole process for each language in the list at the top
for language in languageList:
	engToIndigDict = buildEnglishToIndiginousDictionary(language)

	# Skip if the dictionary wasn't downloaded correctly
	if engToIndigDict == -1:
		continue

	engWords = open("en_GB_wordlist.combined")
	indigWords = open("{0}_wordlist.combined".format(language), 'w')
	indigWords.write('<?xml version="1.0" encoding="UTF8" ?>\n<wordlist>\n')

	# Runs through the english dictionary and checks it against the indiginous words translation
	prog = re.compile("word=([^,]*),f=([^,]*),")
	for line in engWords:
		result = prog.search(line)
		if result:
			eng = result.group(1).lstrip("-")
			freq = result.group(2)

			# If a match is found, write the indiginous word to the xml file with the corresponding english frequency
			if eng in engToIndigDict:
				for indigWord in engToIndigDict[eng]:
					indigWords.write('<w f="{1}">{0}</w>\n'.format(indigWord, freq))

				# Remove each matched word so we are left with all unmatched words at the end
				engToIndigDict.pop(eng)

	# Use a base frequency value for words that don't translate to a single word
	for eng in engToIndigDict:
		for indigWord in engToIndigDict[eng]:
			indigWords.write('<w f="{1}">{0}</w>\n'.format(indigWord, BASE_FREQ))

	indigWords.write('</wordlist>')

	engWords.close()
	indigWords.close()
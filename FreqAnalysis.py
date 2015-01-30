###################################################################################################
#
# This script parses a (preferably large) raw text file containing natural use of the language
# to be analysed. The words used are checked against the supplied official wordlist then frequency
# analysis is performed to determine which words are the most commonly used. The outputted file
# can be run through the java "MakeDict" utility to generate a binary dictionary which can be used
# in a language pack for "AnySoftKeyboard" for Android.
#
# Author: Julian Fell (julian.fell@uq.net.au)
#
###################################################################################################
from math import *
import re
import string

# Option to only count words that appear in a chosen dictionary
MATCH_AGAINST_DICTIONARY = False

# The xml formatted wordslist which defines which words are in the language
OfficialWordsList = "kaytetye dictionary.txt"

# Which format the dictionary file is in. Options: {"Xml", "Backslash"}
WordsListType = "Backslash"

# A raw text file with a *large* amount of natural writing in the language
RawText = "kaytetye.txt"

# What the outputted file will be called
OutputFileName = "test_wordlist2"

#
# Read in a backslash dictionary file and stores it in a list
#
def buildListofRealWordsBackslashFile(filename):
	g = open(filename)

	prog = re.compile("\\\sk (.*)")

	realWords = []
	for line in g:
		result = prog.search(line)
		if result:
			realWords.append(result.group(1))
	return realWords

#
# Read in an xml dictionary file and stores it in a list
#
def buildListofRealWordsXmlFile(filename):
	g = open(filename)

	prog = re.compile("word=([^,]*),")

	realWords = []
	for line in g:
		result = prog.search(line)
		if result:
			realWords.append(result.group(1))
	return realWords

#
# Reads in a textfile and strips it down to a list of words used
#
def parsePlainText(filename):
	f = open(filename, "r")
	text = f.read()
	wordList = [w.lstrip("-") for w in re.split('\W', text.lower()) if w]

	return wordList

#
# Counts up and normalizes the frequency counts
#
def calcFreq(wordList, realWords):
	DICT = {}
	for word in wordList:
		if word in realWords or MATCH_AGAINST_DICTIONARY:
			if word in DICT:
				DICT[word] += 1
			else:
				DICT[word] = 1

	maxFreq = float(max(DICT.values()))

	for key in DICT:
		DICT[key] = int( (255) * (float( DICT[key] )/maxFreq) )
	return DICT

#
# Writes the python dict to an XML file
#
def writeToXmlFile(filename, dictionary):
	indigWords = open(filename, 'w')
	indigWords.write('<?xml version="1.0" encoding="UTF8" ?>\n<wordlist>\n')
		
	for indigWord in dictionary:
		indigWords.write('<w f="{1}">{0}</w>\n'.format(indigWord, DICT[indigWord]))
	indigWords.write('</wordlist>')
	indigWords.close()

########################################################################

if MATCH_AGAINST_DICTIONARY:
	if WordsListType == "Xml"
		realWords = buildListofRealWordsXmlFile(OfficialWordsList)
	elif WordsListType == "Backslash":
		realWords = buildListofRealWordsBackslashFile(OfficialWordsList)
else:
	realWords = []
wordList = parsePlainText(RawText)
DICT = calcFreq(wordList, realWords)
writeToXmlFile(OutputFileName, DICT)


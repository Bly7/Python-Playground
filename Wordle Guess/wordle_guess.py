
# Wordle Guessing Helper Functions
# Author: Bobby Smith
# Date: 2026-1-29

# This module provides functions to help filter and suggest possible Wordle guesses based on given constraints.
# It includes functions to filter words by length, included/excluded letters, and letter positions.
# It also includes a main function to demonstrate the filtering process step-by-step and through a consolidated function.

# Includes

# import necessary libraries
import random

# I've included the dwyl word list in the same directory as this script, because it's a good comprehensive list of English words.
# This can be found at: https://github.com/dwyl/english-words


# import word list from a file
def load_word_list(file_path):
	with open(file_path, 'r') as file:
		words = [line.strip() for line in file.readlines()]
	return words

# filter words by length
def getWordsOfLength(word_list, length):
	return [word for word in word_list if len(word) == length]

# filter words containing a specific letter, regardless of position, frequency and capitalization
def getWordsContainingLetter(word_list, letter):
	return [word for word in word_list if letter.lower() in word.lower()]

# filter words not containing a specific letter, regardless of position, frequency and capitalization
def getWordsNotContainingLetter(word_list, letter):
	return [word for word in word_list if letter.lower() not in word.lower()]

# filter words not containing a spectific letter in a specific position
def getWordsNotContainingLetterInPosition(word_list, letter, position):
	return [word for word in word_list if word[position].lower() != letter.lower()]

# filter words containing a specific letter in a specific position
def getWordsContainingLetterInPosition(word_list, letter, position):
	return [word for word in word_list if word[position].lower() == letter.lower()]

# Give me a random word from the list
def getRandomWord(word_list):
	return random.choice(word_list)

# give me a list of words that do not contain any nonalphabetic characters
def getWordsWithOnlyAlphabeticCharacters(word_list):
	return [word for word in word_list if word.isalpha()]

# Get word containing the most vowels, don't count duplicate vowels as more than one
def getWordWithMostVowels(word_list):
	vowels = 'aeiou'
	max_vowel_count = 0
	word_with_most_vowels = ''
	for word in word_list:
		vowel_count = len(set(letter for letter in word.lower() if letter in vowels))
		if vowel_count > max_vowel_count:
			max_vowel_count = vowel_count
			word_with_most_vowels = word
	return word_with_most_vowels

# remove proper nouns from the list (words that start with a capital letter)
def removeProperNouns(word_list):
	return [word for word in word_list if not word[0].isupper()]

# Wordle Guess List Function
def wordGuessList(word_length: int, included_letters: list, excluded_letters: list, correct_positions: list, incorrect_positions: list) -> list:
	# Load word list
	word_list = load_word_list('words.txt')

	# Filter by word length
	filtered_words = getWordsOfLength(word_list, word_length)

	# filter out non-alphabetic words
	filtered_words = getWordsWithOnlyAlphabeticCharacters(filtered_words)

	# filter out proper nouns
	filtered_words = removeProperNouns(filtered_words)

	# if it is all empty inputs, return word with the most vowels
	if not included_letters and not excluded_letters and not correct_positions and not incorrect_positions:
		return [getWordWithMostVowels(filtered_words)]

	# Filter by included letters
	for letter in included_letters:
		filtered_words = getWordsContainingLetter(filtered_words, letter)

	# Filter by excluded letters
	for letter in excluded_letters:
		filtered_words = getWordsNotContainingLetter(filtered_words, letter)

	# Filter by correct positions (now a list of tuples)
	for position, letter in correct_positions:
		filtered_words = getWordsContainingLetterInPosition(filtered_words, letter, position)

	# Filter by incorrect positions (now a list of tuples)
	for position, letter in incorrect_positions:
		filtered_words = getWordsNotContainingLetterInPosition(filtered_words, letter, position)

	return filtered_words

# main function
def main():
	# First Attempt at step-by-step filtering
	'''
	# Load word list
	word_list = load_word_list('words.txt')
	print(f"Loaded {len(word_list)} words.")

	# Get all 5 character words
	filtered_words = getWordsOfLength(word_list, 5)
	print(f"Number of 5-letter words: {len(filtered_words)}")

	# Get all words containing the letter 'a'
	filtered_words = getWordsContainingLetter(filtered_words, 'a')
	print(f"Number of words containing 'a': {len(filtered_words)}")

	# Get all words not containing 'a' in the 4th position
	filtered_words = getWordsNotContainingLetterInPosition(filtered_words, 'a', 3)
	print(f"Number of words with 'a' not in 4th position: {len(filtered_words)}")

	# Get all words not containing the letter 'e'
	filtered_words = getWordsNotContainingLetter(filtered_words, 'e')
	print(f"Number of words after filtering out 'e': {len(filtered_words)}")

	# Get all words not containing the letter 'd'
	filtered_words = getWordsNotContainingLetter(filtered_words, 'd')
	print(f"Number of words after filtering out 'e' and 'd': {len(filtered_words)}")

	# Get all words not containing the letter 'r'
	filtered_words = getWordsNotContainingLetter(filtered_words, 'r')
	print(f"Number of words after filtering out 'e', 'd' and 'r': {len(filtered_words)}")

	# Get all words not containing the letter 'm'
	filtered_words = getWordsNotContainingLetter(filtered_words, 'm')
	print(f"Number of words after filtering out 'e', 'd', 'r' and 'm': {len(filtered_words)}")

	# get all words containing the letter 'f' in the first position
	filtered_words = getWordsContainingLetterInPosition(filtered_words, 'f', 0)
	print(f"Number of words with 'f' in the first position: {len(filtered_words)}")

	# get all words containing the letter 'y' in the 5th position
	filtered_words = getWordsContainingLetterInPosition(filtered_words, 'y', 4)
	print(f"Number of words with 'y' in the 5th position: {len(filtered_words)}")

	# get all words not containing the letter 'a' in the 2nd position
	filtered_words = getWordsNotContainingLetterInPosition(filtered_words, 'a', 1)
	print(f"Number of words with 'a' not in the 2nd position: {len(filtered_words)}")

	# get all words not containing the letter 'n'
	filtered_words = getWordsNotContainingLetter(filtered_words, 'n')
	print(f"Number of words after filtering out 'n': {len(filtered_words)}")

	# Get a random word from the filtered list
	random_word = getRandomWord(filtered_words)
	print(f"Random word: {random_word}")
	'''

	# First Attempt at using wordGuessList function
	'''
	guess_list = wordGuessList(5, ['a', 'f', 'y'], ['e', 'd', 'r', 'm', 'n'], {0: 'f', 4: 'y'}, {1: 'a'})
	print(f"Possible wordle guesses: {guess_list}")'''

	# second Attempt at using wordGuessList function
	'''
	guess_list2 = wordGuessList(5,['f','l'],['o','c','s'],{0:'f'},{1:'l'})
	random_word2 = getRandomWord(guess_list2)
	print(f"Random wordle guess from all 5-letter words: {random_word2}")
	print(f"Possible wordle guesses: {guess_list2}")'''

	# Third Attempt at using wordGuessList function
	'''
	guess_list = wordGuessList(5, ['o','f', 'r'], ['g', 'a', 'd', 'i','e','u', 'w', 's', 'l', 'b', 'c', 'k'], {2: 'o', 1: 'r', 3: 'o', 4: 'f'}, {1: 'o', 3: 'f', 0: 'f'})
	# list length
	print(f"Number of possible wordle guesses: {len(guess_list)}")
	# get random word from list
	random_word = getRandomWord(guess_list)
	print(f"Random wordle guess from all 5-letter words: {random_word}")'''

	'''
	guess_list = wordGuessList(5, [], [], {}, {})
	word_with_most_vowels = getWordWithMostVowels(guess_list)
	print(f"Word with most vowels from all 5-letter words: {word_with_most_vowels}")
	
	guess_list = wordGuessList(5, ['a', 'i', 'r'], ['d', 'e', 'u', 'k', 'g', 'n', 'm', 'h', 'v', 'l'], {3: 'a', 1: 'i'}, [(0, 'i'), (0, 'a'), (2, 'i'), (1, 'a'), (2, 'r'), (3, 'r'), (4, 'i'), (3, 'i'), (2, 'a'), (1, 'r')])
	guess_list = removeProperNouns(guess_list)

	length_of_list = len(guess_list)
	print('Number of possible guesses:', length_of_list)
	random_word = getRandomWord(guess_list)
	print('Random word from filtered list:', random_word)
	print ('All possible guesses:', guess_list)
	'''

	'''
	guess_list = wordGuessList(5, [], [], {}, {})
	word_with_most_vowels = getWordWithMostVowels(guess_list)
	print(f"Word with most vowels from all 5-letter words: {word_with_most_vowels}")

	guess_list = wordGuessList(5, ['e'], ['a', 'd', 'i', 'u'], {}, [(3, 'e')])

	guess_list = wordGuessList(5, ['e', 'o', 'p'], ['a', 'd', 'i', 'u', 't', 'h'], [(1, 'o'), (4, 'e')], [(3, 'e'), (2, 'p')])
	
	guess_list = removeProperNouns(guess_list)

	length_of_list = len(guess_list)
	print('Number of possible guesses:', length_of_list)
	random_word = getRandomWord(guess_list)
	print('Random word from filtered list:', random_word)
	#print ('All possible guesses:', guess_list)
	'''

	'''
	guess_list = wordGuessList(5, [], [], [], [])
	word_with_most_vowels = getWordWithMostVowels(guess_list)
	print(f"Word with most vowels from all 5-letter words: {word_with_most_vowels}")

	guess_list = wordGuessList(5, ['i'], ['a', 'd', 'e', 'u'], [], [(2, 'i')])

	guess_list = wordGuessList(5, ['i', 'l'], ['a', 'd', 'e', 'u', 'r', 'o', 'c', 's', 'h', 't'], [(1, 'i'), (2, 'l'), (3, 'l')], [(2, 'i'), (3, 'i')])


	guess_list = removeProperNouns(guess_list)

	length_of_list = len(guess_list)
	print('Number of possible guesses:', length_of_list)
	random_word = getRandomWord(guess_list)
	print('Random word from filtered list:', random_word)
	#print ('All possible guesses:', guess_list)
	'''
	
	'''
	guess_list = wordGuessList(5, [], [], [], [])
	word_with_most_vowels = getWordWithMostVowels(guess_list)
	print(f"Word with most vowels from all 5-letter words: {word_with_most_vowels}")

	guess_list = wordGuessList(5, ['o', 'm'], ['a', 'e', 'd', 'i', 'u', 'b', 'x', 't', 'y', 'c', 'r', 'k', 's', 'j', 'n'], [(1, 'o'), (2, 'm')], [])

	guess_list = removeProperNouns(guess_list)

	length_of_list = len(guess_list)
	print('Number of possible guesses:', length_of_list)
	random_word = getRandomWord(guess_list)
	print('Random word from filtered list:', random_word)
	#print ('All possible guesses:', guess_list)

	'''

	guess_list = wordGuessList(5, [], [], [], [])

	guess_list = wordGuessList(5, ['a', 'e', 'n'], ['d', 'i', 'u', 'h', 'v', 'y', 'r', 'l', 'm', 's', 'b', 'g'], [(1, 'e'), (3, 'a'), (4, 'n')], [(1, 'a'), (3, 'e'), (2, 'a'), (2, 'n'), (0, 'n')])

	length_of_list = len(guess_list)
	print('Number of possible guesses:', length_of_list)
	random_word = getRandomWord(guess_list)
	print('Random word from filtered list:', random_word)
	print ('All possible guesses:', guess_list)


if __name__ == "__main__":
	main()
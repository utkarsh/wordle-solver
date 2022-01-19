from collections import defaultdict
from functools import reduce
import operator

words = open('/usr/share/dict/words').readlines()
words = set(filter(lambda x: len(x) == 5, map(lambda x : x.strip(), words)))

letter_counts = defaultdict(int)
words_by_letter_positions = defaultdict(set)
words_by_letters = defaultdict(set)

for word in words:
    for pos,c  in enumerate(word):
        letter_counts[c] += 1
        words_by_letter_positions[(c,pos)].add(word)
        words_by_letters[c].add(word)

known_good_positions = set()
known_bad_positions = set()
known_bad_letters = set()
candidates = words

while (True):    
    # sort words by how common the "new" letters that we are introducing are.
    # want to guess common letters first
    known_letters = set(map(lambda x: x[0], known_bad_positions | known_good_positions))
    def sort_key(word):
        new_letters = set(word) - known_letters
        return reduce(operator.add, map(lambda c: letter_counts[c], new_letters), 0)

    sorted_candidates = sorted(candidates, key = sort_key, reverse = True)

    guess = sorted_candidates[0]
    print("Guess: " + guess)

    while True:
        colors_or_guess = input("Enter the sequence of colors [b(lack),y(ellow),g(reen)] or your own guess ")

        if (len(colors_or_guess) != 5): 
            print("Invalid input")
        elif (len(set(colors_or_guess) - set("gyb")) > 0):
            # contains characters other than gyb, so we'll consider it as a guess
            guess = colors_or_guess
        else:
            colors = colors_or_guess
            break

    if (set(colors) == set('g')):
        # all green, done!
        print("Done")
        break
    
    for pos, color in enumerate(colors):
        if (color == 'g'):
            known_good_positions.add((guess[pos],pos))
        elif (color == 'y'):
            known_bad_positions.add((guess[pos], pos))
        else:
            known_bad_letters.add(guess[pos])
    
    #candidates should have the letters in the known positions
    candidates = reduce(lambda x, y: x.intersection(y), map(lambda x: words_by_letter_positions[x], known_good_positions), candidates)
    
    #candidates should have the letters that are in the word but in bad positions
    candidates = reduce(lambda x, y: x.intersection(y), map(lambda x: words_by_letters[x[0]], known_bad_positions), candidates)
    
    #candidates should NOT have the letters that are in known bad positions
    candidates = reduce(lambda x, y: x.difference(y), map(lambda x: words_by_letter_positions[x], known_bad_positions), candidates)

    #candidates should NOT have the known bad letters
    candidates = reduce(lambda x, y: x.difference(y), map(lambda x: words_by_letters[x], known_bad_letters), candidates)

    if (len(candidates) == 0):
        print("Ran out of valid candidates in dictionary")
        break
from flask import Flask, render_template, request
import json
from datetime import datetime
import time
import collections
app = Flask(__name__)

@app.route('/main')
def hello_world():
    return render_template('hangman.html')

if __name__ == '__main__':
    app.run(debug=True)

# should take the current word in some format and return the new list of words in some format
# right now just testing
# Note: if /word is requested again before the first is finished processing, it will get to work on processing again
# immediately
@app.route('/word')
def wordRoute():
    qstring = request.args.get('word', '')
    word = qstring.lower()
    # DUMMY DATA
    #now = datetime.now()
    #toReturn['letters'] = ['A','E','B','K','C']
    #toReturn['words'] = ['apple','change','chains',str(word),str(now)]
    toReturn = getSuggestions(word)
    return json.dumps(toReturn)

def getSuggestions(word):
    # Should basically take list of words and iterate through it, checking whether it could match the current word
    # check: length first, then each KNOWN letter to check that it matches, otherwise, do not append it to the return list
    # then analyze that list for possible letters
    log = open('/home/ubuntu/projects/hangman_webapp/log.txt', 'a')
    log.write(word+'==================\n')
    toReturn = {'letters':[],'words':[]}
    maybewords = []
    length = len(word)
    with open('/home/ubuntu/projects/hangman_webapp/words_med.txt') as f:
        allWords = f.read().splitlines()
        for maybeword in allWords:
            if len(maybeword) != length:
                continue
            else:
                if not possible(word, maybeword, length, log):
                    continue
            maybewords.append(maybeword)
    #TODO: analyze letter freqs
    bestletters = bestLetters(maybewords)

    maybelen = len(maybewords)
    #ensure list of words is 10 long
    if maybelen > 10:
        temp = ['p','l','a','c','e','h','o','l','d','r']
        for i in range(10):
            temp[i] = maybewords[i]
        maybewords = temp
    elif maybelen < 10:
        diff = 10 - maybelen
        for i in range(diff):
            maybewords.append('')
    toReturn['letters'] = bestletters
    toReturn['words'] = maybewords
    log.close()
    return toReturn

def possible(word, maybeword, length, log):
    log.write(word + ' ' + maybeword + ' ' + str(length) + '\n')
    for i in range(length):
        if word[i] == '_':
            pass
        elif maybeword[i] != word[i]:
            return False
    return True

def bestLetters(words):
    letters = []
    for word in words:
        for char in word:
            letters.append(char)
    c = collections.Counter(letters)
    toReturn = []
    for letter in c.most_common(10):
        toReturn.append(letter[0])
    return toReturn
# to refactor this:
# take the existing hangman script and streamline it
# 2 approaches:
#   make one route/function that will take full word state and return list of letters/words
#       this will require running through whole list of words every new letter (may be slow)
#   use some sort of caching either in browser or in the server so that each session uses one list that shrinks
#   over the course of using it
#       more optimal but more difficult...
# for now let's just make number 1

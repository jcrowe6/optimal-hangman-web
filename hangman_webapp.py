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

@app.route('/word')
def wordRoute():
    qstring = request.args.get('word', '')
    word = qstring.lower()
    toReturn = getSuggestions(word)
    return json.dumps(toReturn)

def getSuggestions(word):
    log = open('/home/ubuntu/projects/hangman_webapp/log.txt', 'a')
    log.write('======== '+word+' ========\n')
    toReturn = {'letters':[],'words':[]}
    maybewords = []
    length = len(word)
    with open('/home/ubuntu/projects/hangman_webapp/words_big.txt') as f:
        allWords = f.read().splitlines()
        for maybeword in allWords:
            if len(maybeword) != length:
                continue
            else:
                if not possible(word, maybeword, length, log):
                    continue
            maybewords.append(maybeword)
    # Returns lis
    bestletters = bestLetters(maybewords, word, log)

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
    for i in range(length):
        if word[i] == '_':
            #pass
            if maybeword[i] in word:
                return False
        elif maybeword[i] != word[i]:
            return False
    return True

def bestLetters(words, word, log):
    letters = {}
    for aWord in words:
        put = []
        for char in aWord:
            if char not in put:
                if char in letters:
                    letters[char] += 1
                else:
                    letters[char] = 1
    # Sorts by value and reverses (so most common occurences appear first)
    full = sorted(letters, key=letters.get)[::-1]

    # Should remove occurences of letters that are already known (broken)
    for i in range(len(full) - 1, -1, -1):
        if full[i] in word:
            log.write("  "+word+'\n')
            full.remove(full[i])

    # ensures length is 10 and returns
    toReturn = []
    lenfull = len(full)
    if lenfull > 10:
        for i in range(10):
            toReturn.append(full[i])
    elif lenfull <= 10:
        toReturn = full
    return toReturn

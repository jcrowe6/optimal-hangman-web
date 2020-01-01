from flask import Flask, render_template
import json
from datetime import datetime
import time
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
def createSuggestions():
    toReturn = {}
    now = datetime.now()
    toReturn['letters'] = ['A','E','B','K','C']
    toReturn['words'] = ['apple','change','chains','yellow',str(now)]
    return json.dumps(toReturn)

# to refactor this:
# take the existing hangman script and streamline it
# 2 approaches:
#   make one route/function that will take full word state and return list of letters/words
#       this will require running through whole list of words every new letter (may be slow)
#   use some sort of caching either in browser or in the server so that each session uses one list that shrinks
#   over the course of using it
#       more optimal but more difficult...
# for now let's just make number 1

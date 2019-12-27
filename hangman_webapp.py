from flask import Flask, render_template
app = Flask(__name__)

@app.route('/main')
def hello_world():
    return render_template('hangman.html')

if __name__ == '__main__':
    app.run(debug=True)

# to refactor this:
# take the existing hangman script and streamline it
# 2 approaches:
#   make one route/function that will take full word state and return list of letters/words
#       this will require running through whole list of words every new letter (may be slow)
#   use some sort of caching either in browser or in the server so that each session uses one list that shrinks
#   over the course of using it
#       more optimal but more difficult...

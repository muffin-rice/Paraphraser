from flask import Flask, request
import app.score_algorithm as score_algorithm
import app.page_parser as page_parser

print('Content-type: text/html\n')

def hello(username = 'World'): 
    return f'<p>Hello sad {username}!'

app = Flask(__name__)


@app.route('/', methods=['GET'])
def paraphrase(): 
    url = request.args.get('url')
    if not url: 
        return 'Welcome to the paraphraser home page!'

    params = request.args.get('keywords')

    if params: 
        params = params.split('!')
    else:
        params = []

    doc = page_parser.scrapeHTML(url)
    
    if doc == '': 
        return 'This website has no text to paraphrase'

    return score_algorithm.summarize(doc, params)

# run the app.
if __name__ == "__main__":

    #application.debug = True
    app.run()
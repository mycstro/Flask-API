from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        app.logger.debug("saying hello")
        with open('data.txt', 'a') as outfile:
            json.dump(data, outfile)
        return 'Data posted'
    else:
        return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)
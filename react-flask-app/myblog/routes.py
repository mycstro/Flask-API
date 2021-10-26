from myblog import app

@app.route('/myblog')
@app.route('/blog')
def index():
    return "Hello, World!"
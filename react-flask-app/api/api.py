from api import app
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
import pandas as pd
import ast, json, time

api = Api(app)

@app.route('/api')
def index():
    return app.send_static_file('index.html')

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

class Data(Resource):
    @app.route('/api/data', methods=['GET'])
    def get(self):
        try:        
            with open('data.json', 'r') as f:
                data = json.load(f)
                if not data:
                    abort(400, message="Could not find any data.")
            return data
        except FileNotFoundError as err:
            return f"Cannot locate file Error: {err}"
        except:
            return "Something went completely wrong"

    @app.route('/api/data', methods=['POST'])
    def post(self):
        data = request.get_json()
        app.logger.info("Applying post.")
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
            post = "Posted data: {0}".format(data)
        return jsonify(post)

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')
    
api.add_resource(Data, '/api/data')

if __name__ == '__main__':
    app.run(debug=True)
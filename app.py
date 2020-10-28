from flask import Flask, jsonify, request
import turing
import json

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/register', methods=['POST'])
def register():
    if(request.method == "POST"):
        data = json.loads(request.json)
        pass
    else:
        return None, 400

@app.route('/login', methods=['POST'])
def login():
    if(request.method == "POST"):
        data = json.loads(request.json)
        pass
    else:
        return None, 400

@app.route('/session/blueprints', methods=['POST'])
def getUserBpcs():
    if(request.method == "POST"):
        data = json.loads(request.json)
        pass
    else:
        return None, 400

@app.route('/session/loadbpc', methods=['POST'])
def loadUserBpc():
    if(request.method == "POST"):
        data = json.loads(request.json)
        pass
    else:
        return None, 400

@app.route('/session/savebpc', methods=['POST'])
def saveUserBpc():
    if(request.method == "POST"):
        data = json.loads(request.json)
        pass
    else:
        return None, 400

@app.route('/session/runbpc', methods=['POST'])
def runBpc():
    if(request.method == "POST"):
        try:
            machine = turing.TuringMachine()
            data = json.loads(request.get_data(parse_form_data=True))

            moves = data.get("moves")
            startPos = data.get("pos")
            startState = data.get("state")
            states = data.get("machine")
            fieldData = data.get("fieldData")

            field = None

            dimensions = fieldData.get("dimensions")
            size = fieldData.get("size")
            values = fieldData.get("values")
            if(values):
                field = turing.Field(dimensions, size, values)
            else:
                filler = fieldData.get("filler")
                field = turing.Field(dimensions, size, filler=filler)

            result = machine.fullExecute(moves, states, field, startState, startPos)

            return json.dumps({"values" : result.array, "dimensions" : result.dimensions, "size" : result.size}), 200
        except Exception as e:
            return str(e), 400
    else:
        return None, 400

@app.route('/session/debug/start', methods=['POST'])
def startDebug():
    if(request.method == "POST"):
        data = json.loads(request.json)
        pass
    else:
        return None, 400

@app.route('/session/debug/step', methods=['POST'])
def stepDebug():
    if(request.method == "POST"):
        data = json.loads(request.json)
        pass
    else:
        return None, 400

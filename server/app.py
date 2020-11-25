from flask import Flask, jsonify, request
from flask_cors import CORS
import turing
import json

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)

class VirtualDB():
    users = {}
    programs = {}
    lastId = 0
    def createUser(self, email: str, password: str, name: str) -> bool:
        if(email not in self.users):
            self.users.update({email : {"password" : password, "name" : name, "programs" : []}})
            return True
        else:
            return False

    def findUser(self, email: str) -> {}:
        return self.users.get(email)

    def saveProgram(self, email: str, program) -> str:
        user = self.users.get(email)
        if(user):
            self.programs.update({str(self.lastId) : program})
            user.get("programs").append(str(self.lastId))
            self.lastId += 1

            return str(self.lastId - 1)

    def loadProgram(self, programId: str) -> {}:
        return self.programs.get(programId)

    def deleteProgram(self, email, programId):
        user = self.users.get(email)
        if(user):
            self.programs.pop(programId)
            user.get("programs").remove(programId)
            
class SessionsManager():
    lastId = 0
    sessions = {}
    
    def createSession(self, email: str) -> str:
        self.sessions.update({str(self.lastId) : {"email" : email, "machine" : turing.TuringMachine()}})
        self.lastId += 1
        return str(self.lastId - 1)

    def getSession(self, token: str) -> {}:
        return self.sessions.get(token)

db = VirtualDB()
sessions = SessionsManager()

@app.route('/register', methods=['POST'])
def register():
    if(request.method == "POST"):
        data = json.loads(request.get_data())

        email = data.get("email")
        password = data.get("password")
        name = data.get("name")

        if(db.createUser(email, password, name)):
            return "User registered successfully", 200
        else:
            return "User with this email already exist", 400

    else:
        return None, 400

@app.route('/login', methods=['POST'])
def login():
    if(request.method == "POST"):
        data = json.loads(request.get_data())
        
        email = data.get("email")
        password = data.get("password")

        token = None
        error = None
        status = 200

        user = db.findUser(email)
        if(user):
            if(user.get("password") == password):
                token = sessions.createSession(email)
            else:
                error = "Wrong password"
                status = 400
        else:
            error = "This email didn't exist"
            status = 400

        return json.dumps({"token" : token, "error": error}), status
    else:
        return None, 400

@app.route('/session/blueprints', methods=['POST'])
def getUserBpcs():
    if(request.method == "POST"):
        data = json.loads(request.get_data())

        token = data.get("token")

        bpcs = None
        error = None
        status = 200

        session = sessions.getSession(token)

        if(session):
            email = session.get("email")
            user = db.findUser(email)
            bpcs = user.get("programs")
        else:
            error = "Wrong token"
            status = 400

        return json.dumps({"blueprints" : bpcs, "error": error}), status
    else:
        return None, 400

@app.route('/session/loadbpc', methods=['POST'])
def loadUserBpc():
    if(request.method == "POST"):
        data = json.loads(request.get_data())
        
        token = data.get("token")
        programId = data.get("id")

        bpc = None
        error = None
        status = 200

        session = sessions.getSession(token)

        if(session):
            program = db.loadProgram(programId)
            if(program):
                bpc = program
            else:
                error = "Wrong id"
                status = 400
        else:
            error = "Wrong token"
            status = 400

        return json.dumps({"bpc" : bpc, "error": error}), status
    else:
        return None, 400

@app.route('/session/deletebpc', methods=['POST'])
def deleteUserBpc():
    if(request.method == "POST"):
        data = json.loads(request.get_data())
        
        token = data.get("token")
        programId = data.get("id")

        status = 200

        session = sessions.getSession(token)

        if(session):
            email = session.get("email")

            db.deleteProgram(email, programId)

            return "BPC deleted succesfully", status
        else:
            error = "Wrong token"
            status = 400
    else:
        return None, 400

@app.route('/session/savebpc', methods=['POST'])
def saveUserBpc():
    if(request.method == "POST"):
        data = json.loads(request.get_data())
        
        token = data.get("token")

        session = sessions.getSession(token)

        if(session):
            email = session.get("email")
            try:
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
            except Exception as e:
                return str(e), 400

            data.update({"fieldData" : field.array})

            db.saveProgram(email, data)

            return "BPC saved succesfully", 200
            
        else:
            return "Wrong token", 400


    else:
        return None, 400

@app.route('/session/runbpc', methods=['POST'])
def runBpc():
    if(request.method == "POST"):
        data = json.loads(request.get_data())
        token = data.get("token")

        session = sessions.getSession(token)

        if(session):
            try:
                machine = session.get("machine")

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
            return "Wrong token", 400
    else:
        return None, 400

@app.route('/session/debug/start', methods=['POST'])
def startDebug():
    if(request.method == "POST"):
        data = json.loads(request.get_data())
        token = data.get("token")

        session = sessions.getSession(token)

        if(session):
            try:
                machine = session.get("machine")

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

                result = machine.startDebug(moves, states, field, startState, startPos)

                return json.dumps(result), 200
            except Exception as e:
                return str(e), 400

        else:
            return "Wrong token", 400
    else:
        return None, 400

@app.route('/session/debug/next', methods=['POST'])
def stepDebug():
    if(request.method == "POST"):
        data = json.loads(request.get_data())
        token = data.get("token")

        session = sessions.getSession(token)

        if(session):
            machine = session.get("machine")

            result = machine.nextState()
            return json.dumps(result), 200
        else:
            return "Wrong token", 400
    else:
        return None, 400

@app.route('/session/alive', methods=['POST'])
def renewToken():
    if(request.method == "POST"):
        data = json.loads(request.get_data())
        pass
    else:
        return None, 400

app.run()

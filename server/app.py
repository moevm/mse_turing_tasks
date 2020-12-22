from flask import Flask, jsonify, request
from flask_cors import CORS
import turing
import json
import database
import multiprocessing

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)

class cloudMongoDb():
    mongo = database.DataBase()
    programs = {}
    users = {}
    lastId = 0

    def __init__(self):
        self.mongo = database.DataBase()
        for user in self.mongo.users:
            self.users.update({user.get("email") : {
                                                  "password": user.get("password"), 
                                                  "name" : user.get("name"), 
                                                  "programs" : {}
                                                  }
            })

    def createUser(self, email: str, password: str, name: str) -> bool:
        try:
            if(email not in self.users):
                self.mongo.insert_user(name, email, password, [" "], [0], "", [])
                self.users.update({email : {"password": password, 
                                                    "name" : name, 
                                                    "programs" : {}}})
                return True
            else:
                return False
        except:
            return False

    def findUser(self, email: str) -> {}:
        try:
            return self.users.get(email)
        except:
            return None

    def saveProgram(self, email: str, name:str, program) -> str:
        user = self.users.get(email)
        if(user):
            userPrograms = user.get("programs")
            programId = userPrograms.get(name)
            if(programId):
                self.programs.update({programId : program})
            else:
                self.programs.update({str(self.lastId) : program})
                user.get("programs").update({name : str(self.lastId)})
                self.lastId += 1

    def loadProgram(self, email, name: str) -> {}:
        user = self.users.get(email)
        if(user):
            userPrograms = user.get("programs")
            programId = userPrograms.get(name)
            if(programId):
                return self.programs.get(programId)
        
        return None

    def deleteProgram(self, email, name):
        user = self.users.get(email)
        if(user):
            userPrograms = user.get("programs")
            programId = userPrograms.get(name)
            if(programId):
                userPrograms.pop(name)
                self.programs.pop(programId)
            
class SessionsManager():
    lastId = 0
    sessions = {}
    
    def createSession(self, email: str) -> str:
        self.sessions.update({str(self.lastId) : {"email" : email, "machine" : turing.TuringMachine()}})
        self.lastId += 1
        return str(self.lastId - 1)

    def getSession(self, token: str) -> {}:
        return self.sessions.get(token)

db = cloudMongoDb()
sessions = SessionsManager()

@app.route('/register', methods=['POST'])
def register():
    if(request.method == "POST"):
        data = json.loads(request.get_data())

        email = data.get("email")
        password = data.get("password")
        name = data.get("name")

        if(db.createUser(email, password, name)):
            return json.dumps("User registered successfully"), 200
        else:
            return json.dumps("User with this email already exist"), 400

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
            bpcs = list(user.get("programs").keys())
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
        bpcName = data.get("name")

        bpc = None
        error = None
        status = 200

        session = sessions.getSession(token)

        if(session):
            email = session.get("email")
            program = db.loadProgram(email, bpcName)
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
        bpcName = data.get("name")

        status = 200

        session = sessions.getSession(token)

        if(session):
            email = session.get("email")

            db.deleteProgram(email, bpcName)

            return json.dumps("BPC deleted succesfully"), status
        else:
            return json.dumps("Wrong token"), 400
    else:
        return None, 400

@app.route('/session/savebpc', methods=['POST'])
def saveUserBpc():
    if(request.method == "POST"):
        data = json.loads(request.get_data())
        
        token = data.get("token")

        bpcName = data.get("name")

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
            data.pop("token")

            db.saveProgram(email, bpcName, data)

            return json.dumps("BPC saved succesfully"), 200
            
        else:
            return json.dumps("Wrong token"), 400


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

                pool = multiprocessing.Pool(processes=1)

                process = pool.apply_async(turing.TuringMachine.fullExecute, (moves, states, field, startState, startPos))
                
                try:
                    result = process.get(timeout = 30)
                except:
                    return json.dumps("Execution timeout"), 400
 
                return json.dumps(result), 200

            except Exception as e:
                return str(e), 400

        else:
            return json.dumps("Wrong token"), 400
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
                breakpoints = data.get("breakpoints")

                field = None

                dimensions = fieldData.get("dimensions")
                size = fieldData.get("size")
                values = fieldData.get("values")
                if(values):
                    field = turing.Field(dimensions, size, values)
                else:
                    filler = fieldData.get("filler")
                    field = turing.Field(dimensions, size, filler=filler)

                result = machine.startDebug(moves, states, field, startState, startPos, breakpoints)

                return json.dumps(result), 200
            except Exception as e:
                return str(e), 400

        else:
            return json.dumps("Wrong token"), 400
    else:
        return None, 400

def skipToBreakpoint(machine):
    return machine.skipToBreakpoint(), machine

@app.route('/session/debug/breakpoint', methods=['POST'])
def nextBreakpoint():
    if(request.method == "POST"):
        data = json.loads(request.get_data())
        token = data.get("token")

        session = sessions.getSession(token)

        if(session):
            machine = session.get("machine")

            pool = multiprocessing.Pool(processes=1)

            process = pool.apply_async(skipToBreakpoint, (machine, ))
                
            try:
                result, machine = process.get(timeout = 30)
            except:
                return json.dumps("Execution timeout"), 400

            session.update({"machine" : machine})
            return json.dumps(result), 200
        else:
            return json.dumps("Wrong token"), 400
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
            return json.dumps("Wrong token"), 400
    else:
        return None, 400

@app.route('/session/alive', methods=['POST'])
def renewToken():
    if(request.method == "POST"):
        data = json.loads(request.get_data())
        pass
    else:
        return None, 400

if __name__ == "__main__":
    app.run()

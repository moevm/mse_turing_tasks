import copy

class Position:
    array = None
    
    def __init__(self, values):
        array = [copy.copy(i) for i in values]
        self.array = array

    def __str__(self):
        return str(self.array)

    def __getitem__(self, i):
        return self.array[i]

    def __setitem__(self, i, value):
        self.array[i] = value

    def __iter__(self):
        return self.array.__iter__()

    def __add__(self, other):
        clone = copy.deepcopy(self)
        for i in range(len(self.array)):
            clone[i] += other[i]

        return clone

    def __sub__(self, other):
        clone = copy.deepcopy(self)
        for i in range(len(self.array)):
            clone[i] -= other[i]

        return clone

    def __radd__(self, other):
        clone = copy.deepcopy(self)
        for i in range(len(self.array)):
            clone[i] += other[i]

        return clone

    def __rsub__(self, other):
        clone = copy.deepcopy(self)
        for i in range(len(self.array)):
            clone[i] -= other[i]

        return clone

    def __iadd__(self, other):
        for i in range(len(self.array)):
            self.array[i] += other[i]

        return self

    def __isub__(self, other):
        for i in range(len(self.array)):
            self.array[i] -= other[i]

        return self
    

class Field:
    array = None
    size = 0
    dimensions = 0
    
    def __init__(self, dimensions, size, values = None, filler = ''):
        array = filler
        if(values):
            array = copy.deepcopy(values)
        else:
            for i in range(dimensions):
                array = [copy.deepcopy(array) for s in range(size)]

        self.dimensions = dimensions
        self.size = size
        self.array = array
    
    def __str__(self):
        return str(self.array)

    def __getitem__(self, position):
        value = self.array
        for i in range(self.dimensions):
            if(position[-1 - i] >= 0):
                value = value[position[-1 - i]]
            else:
                raise IndexError

        return value

    def __setitem__(self, position, value):
        subArray = self.array
        for i in range(self.dimensions - 1):
            if(position[-1 - i] >= 0):
                subArray = subArray[position[-1 - i]]
            else:
                raise IndexError

        subArray[position[0]] = value

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.array.__iter__()
        

class TuringMachine:
    moves = None
    states = None
    field = None
    curState = None
    curPos = None

    def startDebug(self, moves, states, field, stateOnStart, posOnStart):
        self.moves = copy.deepcopy(moves)
        self.states = copy.deepcopy(states)
        self.field = copy.deepcopy(field)
        self.curState =  self.states.get(stateOnStart)
        self.curPos = Position(posOnStart)

        try:
            curRead = self.field[self.curPos]
        except:
            return None

        return {"write" : None, "writePos" : None, "newState" : stateOnStart, "read" : curRead, "readPos" : self.curPos}

    def nextState(self):
        try:
            prevPos = self.curPos
            prevRead = self.field[self.curPos]

            action = self.curState.get(prevRead)

            prevWrite = action.get("write")
            self.field[self.curPos] = prevWrite

            curStateName = action.get("state")
            self.curState = self.states.get(curStateName)

            self.curPos += self.moves.get(action.get("move"))

            curPos = self.curPos
            curRead = self.field[curPos]
        except Exception:
            return None


        return {"write" : prevWrite, "writePos" : prevPos, "newState" : curStateName, "read" : curRead, "readPos" : curPos}

    def fullExecute(self, moves, states, field, stateOnStart, posOnStart):
        moves = copy.deepcopy(moves)
        states = copy.deepcopy(states)
        field = copy.deepcopy(field)
        curPos = Position(posOnStart)
        curState = states.get(stateOnStart)

        try:
            letter = field[curPos]
            action = curState.get(letter)

            while(action):
                field[curPos] = action.get("write")

                curState = states.get(action.get("state"))

                curPos += moves.get(action.get("move"))
                    

                letter = field[curPos]
                action = curState.get(letter)
        except Exception:
            pass

        return field

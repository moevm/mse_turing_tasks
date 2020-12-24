from bson import ObjectId
import pymongo
import json

from typing import List


# class Direction(enum.Enum):
#     STAY = 'N'
#     LEFT = 'L'
#     RIGHT = 'R'
#     UP = 'U'
#     DOWN = 'D'
def get_in_table(states):
    """to DB"""
    table = []
    for state in states:
        d = {'state': state, 'ways': []}
        for way in states[state]:
            action = {
                "symbol": states[state][way]['write'],
                "state": states[state][way]['state'],
                "move": states[state][way]['move']
            }
            d['ways'].append({'symbol': way, 'action': action})
        table.append(d)
    return table


def get_out_table(input_table):
    """from DB"""
    states = {}
    for row in input_table:
        if row['state'] not in states:
            states[row['state']] = {}
        for way in row['ways']:
            states[row['state']][way['symbol']] = {
                'move': way['action']['move'],
                'write': way['action']['symbol'],
                'state': way['action']['state'],
            }
    return states


class Position:
    def __init__(self, x: int = 0, y: int = 0):
        self.x: int = x
        self.y: int = y


class Action:
    def __init__(self, symbol: str, state: str, move: str):
        self.symbol: str = symbol
        self.state: str = state
        self.move: str = move


class Way:
    def __init__(self, symbol: str, action: Action):
        self.symbol: str = symbol
        self.action = action


class State:
    def __init__(self, state: str, ways: List[Way]):
        self.state: str = state
        self.ways: List[Way] = ways


class Program:
    def __init__(self, _program=None, _json=None):
        if _json is not None:
            self.default_position: Position = Position()
            self.id: str = _json['_id']
            self.default_field: List[List[str]] = _json['default_field']
            self.default_position.x = _json['default_position']['x']
            self.default_position.y = _json['default_position']['y']
            self.table_states: List[State] = []
            self.init_table(_json)

        elif _program is not None:
            self.default_position: Position = Position()
            self.id: str = _program.id
            self.default_field: List[List[str]] = _program.default_field
            self.default_position.x = _program.default_position.x
            self.default_position.y = _program.default_position.y
            self.table_states: List[State] = _program.table_states

        else:
            self.default_position: Position = Position()
            self.id: str = ''
            self.default_field: List[List[str]] = []
            self.table_states: List[State] = []

    def to_json(self) -> dict:
        return {
            '_id': self.id,
            'default_field': self.default_field,
            'default_position': {
                'x': self.default_position.x,
                'y': self.default_position.y,
            },
            'table_states': [
                {
                    'state': state.state,
                    'ways': [
                        {
                            'symbol': way.symbol,
                            'action': {
                                'symbol': way.action.symbol,
                                'state': way.action.state,
                                'move': way.action.move
                            }
                        }
                        for way in state.ways
                    ]
                }
                for state in self.table_states
            ]
        }

    def init_table(self, _json):
        for old_state in _json['table_states']:
            ways = []
            for way in old_state['ways']:
                ways.append(
                    Way(
                        way['symbol'],
                        Action(
                            way['action']['symbol'],
                            way['action']['state'],
                            way['action']['move'],
                        )
                    )
                )
            new_state = State(old_state['state'], ways)
            self.table_states.append(new_state)

    def __str__(self):
        return str(self.to_json())


class Session:
    def __init__(self, matrix: List[List[str]], last_position, table_states):
        if matrix == [] and last_position is None and table_states is None:
            self.matrix: List[List[str]] = []
            self.last_position: Position = Position()
            self.table_states: List[State] = []

        else:
            if isinstance(last_position, Position):
                self.last_position: Position = Position(
                    last_position.x, last_position.y
                )
            else:
                self.last_position: Position = Position()
                self.last_position.x = last_position['x']
                self.last_position.y = last_position['y']
            self.matrix: List[List[str]] = matrix

            if len(table_states) > 0:
                if isinstance(table_states[0], dict):
                    self.table_states: List[State] = []
                    self.init_table(table_states)
                else:
                    self.table_states = table_states

    def init_table(self, table):
        for old_state in table:
            ways = []
            for way in old_state['ways']:
                ways.append(
                    Way(
                        way['symbol'],
                        Action(
                            way['action']['symbol'],
                            way['action']['state'],
                            way['action']['move'],
                        )
                    )
                )
            new_state = State(old_state['state'], ways)
            self.table_states.append(new_state)


class User:
    def __init__(self, _user=None, _json=None):
        if _json is not None:
            self.id: str = _json['_id']
            self.name: str = _json['name']
            self.email: str = _json['email']
            self.password: str = _json['password']
            self.programs: List[str] = _json['programs']
            self.session: Session = Session(
                _json['session']['matrix'],
                _json['session']['last_position'],
                _json['session']['table_states'],
            )

        elif _user is not None:
            self.id: str = _user.id
            self.name: str = _user.name
            self.email: str = _user.email
            self.password: str = _user.password
            self.programs: List[str] = _user.programs
            self.session: Session = _user.session

        else:
            self.id: str = ''
            self.name: str = ''
            self.email: str = ''
            self.password: str = ''
            self.programs: List[str] = []
            self.session: Session = Session([], None, None)

    def to_json(self) -> dict:
        return {
            '_id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'programs': self.programs,
            'session': {
                'matrix': self.session.matrix,
                'last_position': {
                    'x': self.session.last_position.x,
                    'y': self.session.last_position.y
                },
                'table_states': [
                    {
                        'state': state.state,
                        'ways': [
                            {
                                'symbol': way.symbol,
                                'action': {
                                    'symbol': way.action.symbol,
                                    'state': way.action.state,
                                    'move': way.action.move
                                }
                            }
                            for way in state.ways
                        ]
                    }
                    for state in self.session.table_states
                ]
            }
        }

    def __str__(self):
        return str(self.to_json())


class DataBase:
    def __init__(self):
        self.__client = pymongo.MongoClient(
            "mongodb+srv://admin:admin@turingcluster.nzveq.mongodb.net/turing?retryWrites=true&w=majority")
        self.__db = self.__client['turing']

        # self.__client = pymongo.MongoClient('localhost', 27017)
        # self.__db = self.__client['turing']

        self.__programs = self.__db['programs']
        self.__users = self.__db['users']

    def insert_user_old(self, user: User) -> str:
        return self.__users.insert_one(User(_user=user).to_json()).inserted_id

    def insert_program_old(self, program_: Program) -> str:
        return self.__programs.insert_one(Program(_program=program_).to_json()).inserted_id

    def insert_user(
            self,
            name: str,
            email: str,
            password: str,
            session_field: List[List[str]],
            session_position: List[int],
            session_states: dict,
            programs: List[int]
    ):
        user = {
            "name": name,
            "email": email,
            "password": password,
            "session": {
                "matrix": session_field,
                "last_position": {
                    'x': session_position[0],
                    'y': session_position[1] if len(session_position) == 2 else None},
                'table_states': get_in_table(session_states)
            },
            "programs": programs
        }
        return self.__users.insert_one(user).inserted_id

    def find_user(self, email: str) -> dict:
        user = self.__users.find_one({'email': email})
        return {
            "_id": user['_id'],
            "name": user['name'],
            "email": user['email'],
            "password": user['password'],
            "session": {
                "matrix": user['session']['matrix'],
                "last_position": [
                    user['session']['last_position']['x'],
                    user['session']['last_position']['y'],
                ],
                "table_states": get_out_table(user['session']['table_states'])
            },
            "programs": user['programs']
        }

    def remove_user(self, email: str):
        return self.__users.delete_one({'email': email}).deleted_count

    def insert_program(self, email: str, field: List[List[str]], position: List[int], states: dict):
        program = {
            'default_field': field,
            'default_position': {
                'x': position[0],
                'y': position[1] if len(position) == 2 else None
            },
            'table_states': get_in_table(states)
        }
        program_id = self.__programs.insert_one(program).inserted_id
        programs = self.find_user(email)['programs']
        programs.append(program_id)
        self.__users.update_one({'email': email}, {
            '$set': {
                'programs': programs
            }
        })
        return program_id

    def find_program(self, id_: str) -> dict:
        program = self.__programs.find_one({'_id': id_})
        return {
            "_id": program['_id'],
            "default_field": program['default_field'],
            "default_position": [
                program['default_position']['x'],
                program['default_position']['y'],
            ],
            "table_states": get_out_table(program['table_states'])
        }

    def remove_program(self, email: str, id_: str):
        programs = self.find_user(email)['programs']
        # print(programs)
        programs.remove(ObjectId(id_))
        self.__users.update_one({'email': email}, {
            '$set': {
                'programs': programs
            }
        })
        return self.__programs.delete_one({'_id': ObjectId(id_)}).deleted_count

    @property
    def users(self) -> List[dict]:
        return list(self.__users.find({}))

    @property
    def programs(self) -> List[dict]:
        return list(self.__programs.find())

    # CRITICAL_ZONE
    def remove(self):
        self.__users.drop()
        self.__programs.drop()


def example_save_program():
    data_base = DataBase()
    # print(len(data_base.programs))
    # for x in data_base.programs:
    #     print(x)

    program_1 = Program()
    program_1.id = '1'
    program_1.default_position = Position(x=2, y=3)
    program_1.default_field = [
        ['2', '3', '4'],
        ['5', '6', '7'],
        ['10', '11', '12'],
    ]
    program_1.table_states = [
        State('q0', [
            Way('s1', Action('s2', 'q1', 'L')),
            Way('s2', Action('s3', 'q2', 'R')),
        ]),
        State('q1', [
            Way('s3', Action('s3', 'q3', 'U')),
            Way('s4', Action('s4', 'q4', 'D')),
        ]),
    ]
    print("Inserted program's id:", data_base.insert_program_old(program_1))
    # for x in data_base.programs:
    #     print(x)
    # print(len(data_base.programs))


def example_load_program(id_: str):
    data_base = DataBase()
    # for x in data_base.programs:
    #     print(x)
    return data_base.find_program(id_)


def example_save_user():
    data_base = DataBase()
    # print(len(data_base.users))
    # for x in data_base.users:
    #     print(x)

    user_1 = User()
    user_1.id = '1'
    user_1.name = 'Kirill'
    user_1.email = 'qweqwe@mail.ru'
    user_1.password = 'qwerty123'
    user_1.session = Session(
        [
            ['2', '3', '4'],
            ['5', '6', '7'],
            ['10', '11', '12'],
        ],
        Position(4, 5),
        [
            State('q0', [
                Way('s1', Action('s2', 'q1', 'L')),
                Way('s2', Action('s3', 'q2', 'R')),
            ]),
            State('q1', [
                Way('s3', Action('s3', 'q3', 'U')),
                Way('s4', Action('s4', 'q4', 'D')),
            ]),
        ]
    )
    user_1.programs = ['1', '2', '3']

    print("Inserted user's id:", data_base.insert_user_old(user_1))
    # for x in data_base.users:
    #     print(x)
    # print(len(data_base.users))


def example_load_user(id_: str):
    data_base = DataBase()
    # for x in data_base.users:
    #     print(x)
    print(data_base.find_user(id_))


if __name__ == "__main__":
    # table = example_load_program('1').to_json()['table_states']
    # print(json.dumps(table, indent=2))
    # out_table = get_out_table(table)
    # print(json.dumps(out_table, indent=2))
    # second = get_in_table(out_table)
    # print(second)
    # print(table == second)
    # print(json.dumps(table) == json.dumps(second))
    # print(data_base.programs)
    # example_save_program()
    table_states = [
        {
          "state": "q0",
          "ways": [
            {
              "symbol": "a",
              "action": {
                "symbol": "b",
                "state": "q0",
                "move": "r"
              }
            }
          ]
        },
        {
          "state": "q1",
          "ways": [
            {
              "symbol": "a",
              "action": {
                "symbol": "a",
                "state": "q1",
                "move": "r"
              }
            },
            {
              "symbol": "b",
              "action": {
                "symbol": "a",
                "state": "q1",
                "move": "r"
              }
            }
          ]
        }
    ]

    data_base = DataBase()
    # r = data_base.insert_program(
    #     'qweqwe@mail.ru',
    #     [
    #         ["0", "0", "0"],
    #         ["0", "0", "0"],
    #         ["0", "0", "0"]
    #     ],
    #     [1, 3],
    #     get_out_table(table_states)
    # )
    # print(r)
    r2 = data_base.remove_program(
        'qweqwe@mail.ru',
        '5fbfcdcc05c2d4ae2fd02b8c'
    )

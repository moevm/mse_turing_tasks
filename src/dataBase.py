import enum

import pymongo
import json

from typing import List


# class Direction(enum.Enum):
#     STAY = 'N'
#     LEFT = 'L'
#     RIGHT = 'R'
#     UP = 'U'
#     DOWN = 'D'


class Position:
    def __init__(self, x: int = 0, y: int = 0):
        self.x: int = x
        self.y: int = y


class Action:
    def __init__(self, symbol: str, state: str, move: str):
        self.symbol: str = symbol
        self.state: str = state
        self.move: str = move


class State:
    def __init__(self, symbol: str, state: str, action: Action):
        self.symbol: str = symbol
        self.state: str = state
        self.action: Action = action


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
                    "symbol": state.symbol,
                    "state": state.state,
                    "action": {
                        "symbol": state.action.symbol,
                        "state": state.action.state,
                        "move": state.action.move
                    }
                }
                for state in self.table_states
            ]
        }

    def init_table(self, _json):
        for old_state in _json['table_states']:
            new_state = State(
                old_state['symbol'],
                old_state['state'],
                Action(
                    old_state['action']['symbol'],
                    old_state['action']['state'],
                    old_state['action']['move']
                )
            )
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
            new_state = State(
                old_state['symbol'],
                old_state['state'],
                Action(
                    old_state['action']['symbol'],
                    old_state['action']['state'],
                    old_state['action']['move']
                )
            )
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
                        "symbol": state.symbol,
                        "state": state.state,
                        "action": {
                            "symbol": state.action.symbol,
                            "state": state.action.state,
                            "move": state.action.move
                        }
                    }
                    for state in self.session.table_states
                ]
            }
        }

    def __str__(self):
        return str(self.to_json())


class DataBase:
    def __init__(self):
        self.__client = pymongo.MongoClient('localhost', 27017)
        self.__db = self.__client['turing']

        self.__programs = self.__db['programs']
        self.__users = self.__db['users']

    def insert_user(self, user: User) -> str:
        return self.__users.insert_one(User(_user=user).to_json()).inserted_id

    def insert_program(self, program_: Program) -> str:
        return self.__programs.insert_one(Program(_program=program_).to_json()).inserted_id

    def find_user(self, id_: str) -> User:
        return User(_json=self.__users.find_one({'_id': id_}))

    def find_program(self, id_: str) -> Program:
        return Program(_json=self.__programs.find_one({'_id': id_}))

    @property
    def users(self) -> List[User]:
        return list(User(_json=x) for x in self.__users.find({}))

    @property
    def programs(self) -> List[Program]:
        return list(Program(_json=x) for x in self.__programs.find())

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
        State('s1', 'q1', Action('s2', 'q2', 'L')),
        State('s2', 'q2', Action('s3', 'q3', 'R')),
        State('s3', 'q3', Action('s4', 'q4', 'U')),
        State('s4', 'q4', Action('s1', 'q1', 'D')),
    ]
    print("Inserted program's id:", data_base.insert_program(program_1))
    # for x in data_base.programs:
    #     print(x)
    # print(len(data_base.programs))


def example_load_program(id_: str):
    data_base = DataBase()
    # for x in data_base.programs:
    #     print(x)
    print(data_base.find_program(id_))


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
            State('s1', 'q1', Action('s2', 'q2', 'L')),
            State('s2', 'q2', Action('s3', 'q3', 'R')),
            State('s3', 'q3', Action('s4', 'q4', 'U')),
            State('s4', 'q4', Action('s1', 'q1', 'D')),
        ]
    )
    user_1.programs = ['1', '2', '3']

    print("Inserted user's id:", data_base.insert_user(user_1))
    # for x in data_base.users:
    #     print(x)
    # print(len(data_base.users))


def example_load_user(id_: str):
    data_base = DataBase()
    # for x in data_base.users:
    #     print(x)
    print(data_base.find_user(id_))


if __name__ == "__main__":
    DataBase().remove()
    example_save_program()
    example_load_program('1')
    example_save_user()
    example_load_user('1')
    exit(0)
    # dataBase = DataBase()
    # programs = dataBase.programs
    # for program in programs:
    #     print(program['_id'])
    # print(dataBase.users)
    old_program = {
        "_id": 1,
        "default_field": [
            [
                "0",
                "0",
                "0"
            ],
            [
                "0",
                "0",
                "0"
            ],
            [
                "0",
                "0",
                "0"
            ]
        ],
        "default_position": {
            "x": 1,
            "y": 2
        },
        "table_states": [
            {
                "symbol": "s1",
                "state": "q1",
                "action": {
                    "symbol": "s2",
                    "state": "q2",
                    "move": "L"
                }
            },
            {
                "symbol": "s2",
                "state": "q2",
                "action": {
                    "symbol": "s3",
                    "state": "q2",
                    "move": "R"
                }
            },
            {
                "symbol": "s3",
                "state": "q2",
                "action": {
                    "symbol": "s2",
                    "state": "q3",
                    "move": "U"
                }
            },
            {
                "symbol": "s2",
                "state": "q3",
                "action": {
                    "symbol": "s3",
                    "state": "q3",
                    "move": "D"
                }
            },
            {
                "symbol": "s3",
                "state": "q3",
                "action": {
                    "symbol": "s1",
                    "state": "q1",
                    "move": "N"
                }
            }
        ]
    }
    program = Program(_json=old_program)
    clone_program = Program(_program=program)
    new_program = program.to_json()
    print('Program -', program.to_json() == clone_program.to_json())
    old_user_json = {
        "_id": "1",
        "name": "Kirill",
        "email": "qweqwe@mail.ru",
        "password": "qwerty123",
        "session": {
            "matrix": [
                [
                    1,
                    2,
                    3
                ],
                [
                    4,
                    5,
                    6
                ],
                [
                    7,
                    8,
                    9
                ]
            ],
            "last_position": {
                "x": 1,
                "y": 2
            },
            "table_states": [
                {
                    "symbol": "s1",
                    "state": "q1",
                    "action": {
                        "symbol": "s2",
                        "state": "q2",
                        "move": "L"
                    }
                },
                {
                    "symbol": "s2",
                    "state": "q2",
                    "action": {
                        "symbol": "s3",
                        "state": "q2",
                        "move": "R"
                    }
                },
                {
                    "symbol": "s3",
                    "state": "q2",
                    "action": {
                        "symbol": "s2",
                        "state": "q3",
                        "move": "U"
                    }
                },
                {
                    "symbol": "s2",
                    "state": "q3",
                    "action": {
                        "symbol": "s3",
                        "state": "q3",
                        "move": "D"
                    }
                },
                {
                    "symbol": "s3",
                    "state": "q3",
                    "action": {
                        "symbol": "s1",
                        "state": "q1",
                        "move": "N"
                    }
                }
            ]
        },
        "programs": [
            "1",
            "2",
            "3"
        ]
    }
    old_user = User(_json=old_user_json)
    clone_user = User(_user=old_user)
    clone_user_json = clone_user.to_json()
    print('User -', old_user_json == clone_user_json)

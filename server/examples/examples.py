import requests
import json

api = "http://127.0.0.1:5000"

pos = [5, 5]
state = "u"
twoDimensionMoves = {"r" : [1, 0], "l" : [-1, 0], "u" : [0, 1], "d" : [0, -1], "s" : [0, 0]}
twoDimensionField = [['0' for i in range(11)] for i in range(11)]
langton = {
            "u" : 
                {
                    "0" : 
                        {
                            "move" : "r", 
                            "write" : "1",
                            "state" : "r"
                        },
                    "1" : 
                        {
                            "move" : "l", 
                            "write" : "0",
                            "state" : "l"
                        }
                },
            "r" : 
                {
                    "0" : 
                        {
                            "move" : "d", 
                            "write" : "1",
                            "state" : "d"
                        },
                    "1" : 
                        {
                            "move" : "u", 
                            "write" : "0",
                            "state" : "u"
                        }
                },
            "d" : 
                {
                    "0" : 
                        {
                            "move" : "l", 
                            "write" : "1",
                            "state" : "l"
                        },
                    "1" : 
                        {
                            "move" : "r", 
                            "write" : "0",
                            "state" : "r"
                        }
                },
            "l" : 
                {
                    "0" : 
                        {
                            "move" : "u", 
                            "write" : "1",
                            "state" : "u"
                        },
                    "1" : 
                        {
                            "move" : "d", 
                            "write" : "0",
                            "state" : "d"
                        }
                }
        }

timeout = {
            "u" : 
                    {
                        "0" : 
                            {
                                "move" : "s", 
                                "write" : "0",
                                "state" : "u"
                            }
                    }
}


email = "example@example.com"
password = "qwerty"

automatData = {"moves" : twoDimensionMoves, 
               "pos" : pos, 
               "state" : state, 
               "machine" : langton, 
               "fieldData" : {"dimensions" : 2, 
                               "size" : 11,
                               "values" : twoDimensionField}
                }
automatData2 = {"moves" : twoDimensionMoves, 
               "pos" : pos, 
               "state" : state, 
               "machine" : timeout, 
               "fieldData" : {"dimensions" : 2, 
                               "size" : 11,
                               "values" : twoDimensionField}
                }

def reg_example():
    data = {"email" : email, "password" : password, "name" : "example"}
    response = requests.post(api + "/register", data=json.dumps(data))
    print(response.content)

def get_token_example():
    data = {"email" : email, "password" : password}
    response = requests.post(api + "/login", data=json.dumps(data))
    content = response.json()

    token = content.get("token")

    print(content)

    return token

def saving_example(token):
    data = {"token" : token, "name" : "Test BPC"}
    data.update(automatData)

    response = requests.post(api + "/session/savebpc", data=json.dumps(data))
    print(response.content)

    data = {"token" : token, "name" : "Test BPC"}
    data.update(automatData2)

    response = requests.post(api + "/session/savebpc", data=json.dumps(data))
    print(response.content)

def getting_bpc_list_example(token):
    data = {"token" : token}
    response = requests.post(api + "/session/blueprints", data=json.dumps(data))
    content = response.json()
    print(content)

    return content.get("blueprints")

def loading_example(token):
    blueprints = getting_bpc_list_example(token)
    if(len(blueprints)):
        data = {"token" : token, "name" : blueprints[0]}
        response = requests.post(api + "/session/loadbpc", data=json.dumps(data))
        content = response.json()
        print(content)

def deleting_example(token):
    blueprints = getting_bpc_list_example(token)
    if(len(blueprints)):
        data = {"token" : token, "name" : blueprints[0]}
        response = requests.post(api + "/session/deletebpc", data=json.dumps(data))
        print(response.content)

def run_example(token):
    data = {"token" : token}
    data.update(automatData)

    response = requests.post(api + "/session/runbpc", data=json.dumps(data))
    content = response.json()
    print(content)

def debug_example(token, breakpoints):
    data = {"token" : token, "breakpoints" : breakpoints}
    data.update(automatData)
    
    response = requests.post(api + "/session/debug/start", data=json.dumps(data))
    content = response.json()
    print(content)

    data = {"token" : token}
    while(content):
        response = requests.post(api + "/session/debug/breakpoint", data=json.dumps(data))
        content = response.json()
        print(content)

        response = requests.post(api + "/session/debug/next", data=json.dumps(data))
        content = response.json()
        print(content)

if __name__ == "__main__":
    reg_example()
    token = get_token_example()

    saving_example(token)
    #loading_example(token)
    #deleting_example(token)
    #run_example(token)
    #debug_example(token, [[3, 6], [5, 9]])
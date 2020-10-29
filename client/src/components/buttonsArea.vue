<template>
  <div class="buttons">
    <b-container>
      <b-row class="text-center py-3">

        <b-col>
          <b-button class="change" size="sm" variant="warning">Change dimension</b-button>
        </b-col>
        <b-col>
          <b-button @click="startMachine" size="sm" class="start" variant="success">Start/Continue</b-button>
        </b-col>
      </b-row>

      <b-row class="text-center py-3">
        <b-col>
          <b-button class="openFile">Open file</b-button>
        </b-col>
        <b-col>
          <b-button class="Stop" variant="danger">Stop</b-button>
        </b-col>
      </b-row>

      <b-row class="text-center py-3">
        <b-col>
          <b-button class="save">Save file</b-button>
        </b-col>
        <b-col>
          <b-button class="step" variant="primary">Step</b-button>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import axios from 'axios';
import {bus} from '@/main';

export default {
  name: "buttonsArea",
  data() {
    return {
      response: {},
      errors: [],
      ribbonText: 'abababa',
      oneDimension: true,
      table: "",
      fieldSize: 0,
      startPosition: "",
      serverRequest: {
        "moves": {},
        "pos": [],
        "state": "",
        "machine": {},
        "fieldData": {
          "dimensions": 1,
          "size": 1,
          "values": []
        }
      },
      example: {
        "moves": {"d": [0, -1], "s": [0, 0], "u": [0, 1], "r": [1, 0], "l": [-1, 0]},
        "pos": [5, 5],
        "state": "u",
        "machine": {
          "u":
              {
                "0":
                    {
                      "move": "r",
                      "write": "1",
                      "state": "r"
                    },
                "1":
                    {
                      "move": "l",
                      "write": "0",
                      "state": "l"
                    }
              },
          "r":
              {
                "0":
                    {
                      "move": "d",
                      "write": "1",
                      "state": "d"
                    },
                "1":
                    {
                      "move": "u",
                      "write": "0",
                      "state": "u"
                    }
              },
          "d":
              {
                "0":
                    {
                      "move": "l",
                      "write": "1",
                      "state": "l"
                    },
                "1":
                    {
                      "move": "r",
                      "write": "0",
                      "state": "r"
                    }
              },
          "l":
              {
                "0":
                    {
                      "move": "u",
                      "write": "1",
                      "state": "u"
                    },
                "1":
                    {
                      "move": "d",
                      "write": "0",
                      "state": "d"
                    }
              }
        },
        "fieldData":
            {
              "dimensions": 2,
              "size": 11,
              "filler": "0"
            }
      }
    }
  },
  mounted() {
    bus.$on('ribbonChanged', data => {
      this.ribbonText = data
      // console.log("ribbonChanged")
    })

    bus.$on('matrixChanged', data => {
      this.fieldSize = data.fieldSize
      this.startPosition = data.startPosition
    })

    bus.$on('tableChanged', data => {
      this.table = data;
      // console.log("tableChanged")
    })

    bus.$on('changeDimension', data => {
      this.oneDimension = data !== "2d";
    })
  },
  methods: {
    fillRequest() {
      bus.$emit('loadTable')
      if (this.oneDimension) {
        this.serverRequest.fieldData.dimensions = 1
        this.serverRequest.fieldData.size = this.ribbonText.length
        this.serverRequest.moves = {"l": [-1], r: [1], s: [0]}
        this.serverRequest.fieldData.values = this.ribbonText.split("")
        // change later
        this.serverRequest.pos = [0]
      } else {
        this.serverRequest.fieldData.dimensions = 2
        this.serverRequest.fieldData.size = this.fieldSize
        this.serverRequest.moves = {"d": [0, -1], "s": [0, 0], "u": [0, 1], "r": [1, 0], "l": [-1, 0]}
        this.serverRequest.pos = this.startPosition.split(", ").map(parseInt)
        for (let i = 0; i < this.fieldSize; i++) {
          this.serverRequest.fieldData.values.push([...Array(this.fieldSize)].map(() => {
            return 0
          }))
        }
        this.serverRequest.fieldData.filler = 0
      }

      for (let i = 1; i < this.table.length; i++) {
        this.serverRequest.machine[this.table[i][0]] = {}
        for (let j = 1; j < this.table[0].length; j++) {
          let splitted = this.table[i][j].split(", ")
          // console.log(splitted, this.table[i][j])
          if (splitted.length !== 3) {
            throw new TypeError("incorrect table filling")
          }

          this.serverRequest.machine[this.table[i][0]][this.table[0][j]] = {
            "move": splitted[0],
            "write": splitted[1],
            "state": splitted[2]
          }
          // console.log(this.serverRequest.machine[this.table[i][0]][this.table[0][j]])
        }
      }

      this.serverRequest.state = this.table[1][0]

    },
    startMachine() {
      // example request
      try {
        // console.log(this.table)
        this.fillRequest()
        // console.log(this.serverRequest)
        bus.$emit("clicked", "запущен полный прогон машины");
        axios.post('https://wintari.pythonanywhere.com/session/runbpc',
            this.serverRequest,
            {
              headers: {
                'Content-Type': 'application/json'
              }
            }
        )
            .then(response => {
              this.response = response.data;
              console.log(this.response)
              bus.$emit("getAnswer", "получен ответ от сервера");
              if (this.response.dimensions === 1) {
                bus.$emit("getAnswer", this.response.values.join(""));
              } else {
                for(let i = 0; i < this.response.size; i++) {
                  bus.$emit("getAnswer", this.response.values[i].join(""));
                }
              }

              // console.log(this.response)
              // bus.$emit("draw scene", this.response.values);
            })
            .catch(e => {
              console.error(e)
              this.errors.push(e)
            })
      } catch (e) {
        bus.$emit("clicked", "таблица заполнена не правильно");
        console.error(e)
      }
    }
  }
}
</script>

<style scoped>
.buttons {
  border: 2px solid #000000;
  min-width: 35vh;
  height: 35vh;
}
</style>

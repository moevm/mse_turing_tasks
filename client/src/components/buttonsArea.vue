<template>
  <div class="buttons">
    <b-container>
      <b-row class="text-center py-3">

        <b-col>
          <b-button @click="changeDimension" class="change">Change dimension</b-button>
        </b-col>
        <b-col>
          <b-button @click="startMachine" class="start" variant="success">Start/Continue</b-button>
        </b-col>
      </b-row>

      <b-row class="text-center py-3">
        <b-col>
          <b-button class="openFile">Open file</b-button>
        </b-col>
        <b-col>
          <b-button class="step" variant="success">Step</b-button>

        </b-col>
      </b-row>

      <b-row class="text-center py-3">
        <b-col>
          <b-button class="save">Save file</b-button>
        </b-col>
        <b-col>
          <b-button class="Stop" variant="danger">Stop</b-button>
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
      api: 'https://wintari.pythonanywhere.com',
      // api: 'http://127.0.0.1:5000',
      response: {},
      errors: [],

      ribbonText: ' abababa',
      matrix: [],
      oneDimension: true,
      table: "",
      fieldSize: 0,
      startPosition: [0],
      serverRequest: {
        "token": '',
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
        'token': '0',
        "moves": {"u": [0, -1], "s": [0, 0], "d": [0, 1], "r": [1, 0], "l": [-1, 0]},
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
      },
      //

    }
  },
  created() {

  },
  mounted() {
    bus.$on('startPosition', data => {
      this.startPosition = data.point;
    })

    bus.$on('ribbonChanged', data => {
      this.ribbonText = data
    })

    bus.$on('matrixChanged', data => {
      this.fieldSize = data.fieldSize
      this.startPosition = data.startPosition
    })

    bus.$on('tableChanged', data => {
      this.table = data;
    })

    bus.$on('changeDimension', data => {
      this.oneDimension = data !== "2d";
    })

    bus.$on('login', data => {
      this.token = data.token;
    })

    bus.$on('loadMatrix', data => {
      this.matrix = data.matrix
    })
  },
  methods: {
    clearData() {
      this.serverRequest.moves = {}
      this.serverRequest.state = ''
      this.serverRequest.machine = {}
      this.serverRequest.fieldData.values = []

    },
    changeDimension() {
      bus.$emit("dimensionChanged", {oneDimension: !this.oneDimension})
      this.oneDimension = !this.oneDimension
    },
    fillRequest() {
      bus.$emit('loadTable')
      if (this.oneDimension) {
        this.serverRequest.moves = {'l': [-1], 'r': [1], 's': [0]}

        this.serverRequest.fieldData = {
          dimensions: 1,
          size: this.ribbonText.length,
          values: Array(...this.ribbonText.split(""))
        }
        console.log(this.ribbonText.split(""))
      } else {
        bus.$emit('getMatrix')
        this.serverRequest.fieldData = {
          dimensions: 2,
          size: this.matrix.length,
          values: this.matrix
        }
        this.serverRequest.moves = {"u": [0, -1], "s": [0, 0], "d": [0, 1], "r": [1, 0], "l": [-1, 0]}
      }
      this.serverRequest.pos = this.startPosition

      for (let i = 1; i < this.table.length; i++) {
        this.serverRequest.machine[this.table[i][0]] = {}
        for (let j = 1; j < this.table[0].length; j++) {
          let splitted = this.table[i][j].split(",")
          if (splitted.length !== 3 || splitted[0].length != 1 && splitted[1].trim() !== '\\s') {
            throw new TypeError("incorrect table filling")
          }
          let y = this.table[i][0] === "\\s" ? ' ' : this.table[i][0]
          let x = this.table[0][j] === "\\s" ? ' ' : this.table[0][j]
          this.serverRequest.machine[y][x] = {
            "move": splitted[0],
            "write": splitted[1].trim() === "\\s" ? ' ' : splitted[1].trim(),
            "state": splitted[2].trim()
          }
        }
      }

      this.serverRequest.state = this.table[1][0]
      this.serverRequest.token = localStorage.getItem('token')
      console.log('fieldData', this.serverRequest.fieldData)
      console.log('values', this.serverRequest.fieldData.values)
      console.log('moves', this.serverRequest.moves)
      console.log('machine', this.serverRequest.machine)
      console.log('state', this.serverRequest.state)
      console.log('pos', this.serverRequest.pos)
      console.log('token', this.serverRequest.token)
    },
    startMachine() {
      // bus.$emit("draw scene", {dimension: true, body: 'this.response.values'});
      try {
        this.fillRequest()
        this.example.token = localStorage.getItem('token')
        bus.$emit("clicked", "запущен полный прогон машины");
        console.log(`${this.api}/session/runbpc`)
        axios.post(`${this.api}/session/runbpc`,
            this.serverRequest
            , {
              headers: {
                'Content-Type': 'application/json'
              },
            }
        )
            .then(response => {
              console.log('get response')
              this.response = response.data;
              console.log(this.response)
              bus.$emit("getAnswer", "получен ответ от сервера");
              if (this.response.dimensions === 1) {
                bus.$emit("getAnswer", this.response.values.join(""));
              } else {
                for (let i = 0; i < this.response.size; i++) {
                  bus.$emit("getAnswer", this.response.values[i].join(""));
                }
              }
              bus.$emit("drawScene", {dimension: this.oneDimension, body: this.response.values});
            })
            .catch(e => {
              console.error(e)
              console.error(e.name)
              console.error(e.message)
              this.errors.push(e.stack)
              bus.$emit("clicked", "нет ответа от сервера");
            })
      } catch (e) {
        bus.$emit("clicked", "таблица заполнена не правильно");
        console.error(e.name)
      } finally {
        this.clearData()
      }
    }
  }
}
</script>

<style scoped>
.buttons {
  /*border: 2px solid #000000;*/
  min-width: 45vh;
  /*height: 35vh;*/
}

.start, .change, .openFile, .Stop, .save, .step {
  width: 170px;
  height: 30px;
}
</style>

<template>
  <div class="buttons">
    <b-container>
      <b-row class="text-center py-3">

        <b-col>
          <b-button
              @click="changeDimension"
              class="change"
          >Change dimension
          </b-button>
        </b-col>
        <b-col>
          <b-button
              @click="startMachine"
              class="start"
              variant="success"
          >Run
          </b-button>
        </b-col>
      </b-row>

      <b-row class="text-center py-3">
        <b-col>
          <b-button
              class="load"
              @click="getMachines"
              v-b-modal.modalLoadScreen
          >Load Machine
          </b-button>
        </b-col>
        <b-col>
          <b-button
              class="step"
              variant="success"
              @click="stepByStep"
          >Start/Step
          </b-button>

        </b-col>
      </b-row>

      <b-row class="text-center py-3">
        <b-col>
          <b-button
              class="save"
              v-b-modal.saveModal
          >Save machine
          </b-button>
        </b-col>
        <b-col>
          <b-button
              class="Stop"
              variant="danger"
              @click="stopDebug"
          >Stop
          </b-button>
        </b-col>
      </b-row>
    </b-container>
    <b-modal
        id="modalLoadScreen"
        ref="modalLoadScreen"
        title="Choose machine"
    >
      <b-list-group>
        <b-list-group-item
            button
            v-for="machine in userMachinesList"
            :key="machine.id"
            @click="loadMachine(machine)"
        >
          {{ machine }}
        </b-list-group-item>
      </b-list-group>
    </b-modal>
    <b-modal
        id="saveModal"
        ref="saveModal"
        title="Enter machine name"
        @click="saveMachine"
        @ok="okHandle"
    >
      <form @submit.stop.prevent="save">
        <b-form-input
            id="saveInput"
            ref="saveInput"
            v-model="savingName"
            invalid-feedback="Name is required"
            type="text"
            required
            placeholder="Enter machine name"
        ></b-form-input>
      </form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import {bus} from '@/main';

export default {
  name: "buttonsArea",
  data() {
    return {
      api: 'http://127.0.0.1:5000',
      response: {},
      errors: [],
      loadingModalShow: false,
      userMachinesList: [],
      savingName: 'newMachine',
      ribbonText: ' abababa',
      debugPoints: [],
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
      changed: true,
      started: false,
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

    bus.$on('getBreakpointsAnswer', data => {
      this.debugPoints = data
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
      this.$emit("end")
      this.started = false
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
    },
    getDate() {
      let date = new Date()
      return `[${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}.${date.getMilliseconds()}]`
    },
    stopDebug() {
      this.started = false
      bus.$emit('end')
    },

    okHandle(bvModalEvt) {
      bvModalEvt.preventDefault()
      if (this.savingName === "") {
        return
      }
      this.$nextTick(() => {
        this.$bvModal.hide('saveModal')
        this.saveMachine()
      })
    },

    saveMachine() {
      if (this.savingName === null) {
        return
      }
      this.fillRequest()
      this.serverRequest.name = this.savingName
      axios.post(`${this.api}/session/savebpc`,
          this.serverRequest
          , {
            headers: {
              'Content-Type': 'application/json'
            }
          })
          .then(response => {
            console.log(response)
            bus.$emit('getAnswer',
                `${this.getDate()} success save!`)
          })
          .catch(e => {
            this.started = false
            console.error(e)
            this.errors.push(e.stack)
            bus.$emit('end')

          })
    },

    loadMachine(machine) {
      axios.post(`${this.api}/session/loadbpc`,
          {"token": localStorage['token'], "name": machine}
          , {
            headers: {
              'Content-Type': 'application/json'
            }
          })
          .then(response => {
            if (response.data.error !== null) {
              throw Error
            }
            this.serverRequest = response.data.bpc
            this.$refs['modalLoadScreen'].hide()
            this.initLoadedMachine()
            bus.$emit('getAnswer',
                `${this.getDate()} ${machine} loaded!`)
          })
          .catch(e => {
            this.started = false
            console.error(e)
            bus.$emit('end')

          })
    },

    getMachines() {
      this.loadingModalShow = true
      axios.post(`${this.api}/session/blueprints`,
          {"token": localStorage['token']}
          , {
            headers: {
              'Content-Type': 'application/json'
            }
          })
          .then(response => {
            if (response.error != null)
              throw Error
            this.userMachinesList = response.data.blueprints
          })
          .catch(e => {
            this.started = false
            console.error(e)
            bus.$emit('end')

          })
    },

    initLoadedMachine() {
      bus.$emit("drawScene", {
        dimension: this.serverRequest.pos.length !== 2,
        body: this.serverRequest.fieldData
      })
      bus.$emit("setTable", {table: this.serverRequest.machine})
    },

    stepByStep() {
      try {
        if (!this.started) {
          this.fillRequest();
          bus.$emit("getBreakpoints")
          this.serverRequest.breakpoints = this.debugPoints

          axios.post(`${this.api}/session/debug/start`,
              this.serverRequest
              , {
                headers: {
                  'Content-Type': 'application/json'
                }
              })
              .then(response => {
                this.started = true
                console.log(response)
                bus.$emit('started', response.data)
                bus.$emit('getAnswer',
                    `${this.getDate()} launch debug`)
              })
              .catch(e => {
                console.error(e)
                this.started = false
                bus.$emit('end')
              })
        } else {
          if (this.debugPoints.length !== 0) {
            axios.post(`${this.api}/session/debug/breakpoint`,
                {"token": localStorage['token']}
                , {
                  headers: {
                    'Content-Type': 'application/json'
                  }
                })
                .then(response => {
                  bus.$emit("drawScene", {
                    dimension: response.data.dimensions === 1,
                    body: response.data.values,
                    breakpoints: this.debugPoints,
                    newPos: response.data.newPos,
                  })

                })
                .catch(e => {
                  console.error(e)
                  bus.$emit('end')
                })
          }
          setTimeout(() => {
            axios.post(`${this.api}/session/debug/next`,
                {"token": localStorage['token']}
                , {
                  headers: {
                    'Content-Type': 'application/json'
                  }
                })
                .then(response => {
                  console.log(response)
                  if (response.data === null) {
                    this.started = false
                    console.log('about to end')
                    console.log('leng', this.response.length)
                    if (this.response.data !== undefined) {
                      if ( this.oneDimension) {
                        bus.$emit('getAnswer',
                            `${this.getDate()} break point: x=${this.response.data.newPos[0]} | New state '${this.response.data.newState}'`)
                      } else {
                        bus.$emit('getAnswer',
                            `${this.getDate()} break point: x=${this.response.data.newPos[0]} y=${this.response.data.newPos[1]} | New state '${this.response.data.newState}'`)
                      }

                      bus.$emit('stepByStep', {oldPos: this.response.data.newPos, write: this.response.data.write})
                      bus.$emit('getAnswer',
                          `${this.getDate()} process finished!`)
                    }
                    bus.$emit("end")
                    if (this.oneDimension) {
                      bus.$emit('getAnswer',
                          `${this.getDate()} point: x=${response.data.oldPos[0]} | New state '${response.data.newState}'`)
                    } else {
                      bus.$emit('getAnswer',
                          `${this.getDate()} point: x=${response.data.oldPos[0]} y=${response.data.oldPos[1]} | New state '${response.data.newState}'`)
                    }

                  } else {
                    this.response = response
                    bus.$emit('stepByStep', response.data)
                    if (this.oneDimension) {
                      bus.$emit('getAnswer',
                          `${this.getDate()} point: x=${response.data.oldPos[0]} | New state '${response.data.newState}'`)
                    } else {
                      bus.$emit('getAnswer',
                          `${this.getDate()} point: x=${response.data.oldPos[0]} y=${response.data.oldPos[1]} | New state '${response.data.newState}'`)
                    }
                  }

                })
                .catch(e => {
                  this.started = false
                  console.error(e)
                  bus.$emit('end')
                })
          }, 200)

        }
      } catch (e) {
        bus.$emit('getAnswer',
            `${this.getDate()} incorrect table arguments!'`)
        console.error(e.name)
        bus.$emit('end');
      }
    },

    startMachine() {
      try {
        this.fillRequest()
        this.example.token = localStorage.getItem('token')
        bus.$emit("getAnswer", `${this.getDate()} full run of the machine started`);
        axios.post(`${this.api}/session/runbpc`,
            this.serverRequest
            , {
              headers: {
                'Content-Type': 'application/json'
              },
            })
            .then(response => {
              this.response = response.data;
              bus.$emit('getAnswer',
                  `${this.getDate()} get answer from server'`)
              if (this.response.dimensions === 1) {
                bus.$emit("getAnswer", `${this.getDate()} result is\n${this.response.values.join("")}`);
              } else {
                bus.$emit("getAnswer", `${this.getDate()} result is`);
                for (let i = 0; i < this.response.size; i++) {
                  bus.$emit("getAnswer", this.response.values[i].join(""));
                }
              }
              bus.$emit("drawScene", {dimension: this.oneDimension, body: this.response.values});
            })
            .catch(e => {
              console.error(e)
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

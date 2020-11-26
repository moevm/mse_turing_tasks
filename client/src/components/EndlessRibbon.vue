<template @blur="$emit('blur')">
  <div class="local">
<!--    <b-row>-->
    <b-col class="text-center justify-content-md-center w3-border-red">
        <b-form-spinbutton
            @change="matrixChanged"
            v-if="selected==='2d'"
            id="x-step"
            v-model="value_x"
            min="2"
            max="100"
            step="1"
        ></b-form-spinbutton>
      </b-col>
<!--    </b-row>-->
    <div v-if="selected==='2d'">
      <v-stage
          id="canvasMatrix"
          ref="stage"
          :config="configKonvaMatrix"
          @click="startPositionMatrixChanged"
      >
        <v-layer ref="layer">
          <v-rect
              v-for="item in listMatrix"
              :key="item.id"
              v-on:keyup="keyEvent"
              v-on:keypress="keyEvent"
              :config="{
                x: item.x,
                y: item.y,
                width: item.size,
                height: item.size,
                stroke: 'black',
                fill: item.color,
          }"
          ></v-rect>
          <v-text
              v-for="symbol in listMatrix"
              :key="symbol.value_id"
              :config="{
                x: symbol.x + matrixText.offset_x,
                y: symbol.y + matrixText.offset_y,
                text: symbol.value,
                fontSize: matrixText.fontSize,
                listening: false
            }"
          ></v-text>
        </v-layer>
      </v-stage>
    </div>
    <div v-if="selected==='ribbon'">
      <v-stage
          id="canvasRibbon"
          ref="stageRibbon"
          :config="configKonvaRibbon"
          @click="startPositionRibbonChanged"
      >
        <v-layer ref="layer">
          <v-rect
              v-for="item in listRibbon"
              :key="item.id"
              :config="{
                  x: item.x,
                  y: item.y,
                  width: item.size,
                  height: item.size,
                  cornerRadius: 10,
                  stroke: 'black',
                  strokeWidth: 3,
                  fill: item.color === 'white'? 'white':'green'
              }"
          ></v-rect>
          <v-text
              v-for="symbol in listRibbon"
              :key="symbol.value_id"
              :config="{
            x: symbol.x + symbol.offset_x,
            y: symbol.y + symbol.offset_y,
            text: symbol.value,
            fontSize: 30,
            listening: false
            }"
          ></v-text>
        </v-layer>
      </v-stage>
    </div>
  </div>
</template>

<script>
import {bus} from "@/main"

const widthMatrix = window.innerWidth / 3.6;
const heightMatrix = window.innerWidth / 3.6;
export default {
  name: "EndlessRibbon",
  data() {
    return {
      selected: 'ribbon',
      options: [
        {value: 'ribbon', text: 'Лента'},
        {value: '2d', text: 'Двумерная плоскость'}
      ],
      matrix: [],
      // field: "",
      value_x: 8,
      ribbonText: " abababa",
      configKonvaMatrix: {
        width: widthMatrix,
        height: heightMatrix
      },
      matrixText: {
        fontSize: 45,
        offset_x: 10,
        offset_y: 5,
      },
      configKonvaRibbon: {
        width: widthMatrix,
        height: 75
      },
      listMatrix: [],
      listRibbon: [],
      index: 0
    }
  },
  created() {
    // console.log(window.innerHeight, window.innerWidth)
  },
  mounted() {
    bus.$on('drawScene', data => {
      this.selected = data.dimension ? 'ribbon' : '2d'
      if (this.selected === 'ribbon') {
        this.ribbonText = data.body.join("")
      } else {
        this.matrix = data.body
      }
      this.redraw()
    })

    bus.$on('dimensionChanged', data => {
      if (data.oneDimension) {
        this.selected = 'ribbon'
        this.listMatrix[this.index].color = 'white'
      } else {
        this.selected = '2d'
        this.listRibbon[this.index].color = 'white'
      }
      this.index = 0;
    })

    bus.$on('getMatrix', () => {
      let matrix = Array()
      for(let i = 0; i < this.value_x; i++) {
        matrix[matrix.length] = [...Array(this.value_x)]
        for(let j = 0; j < this.value_x; j++) {
          matrix[i][j] = this.listMatrix[j + i * this.value_x].value
        }
      }
      console.log(matrix)
      bus.$emit('loadMatrix', {matrix: matrix})
    })

    document.addEventListener('keyup', (event) => this.keyEvent(event))
    this.createRectangles()
    this.createRibbon()
  },
  methods: {
    createRectangles() {
      this.listMatrix = [];
      this.matrixText = {
        fontSize: 300 / this.value_x,
        offset_x: 200 /this.value_x,
        offset_y: 100 / this.value_x
      }
      for (let y = 0; y < this.value_x; y++) {
        for (let x = 0; x < this.value_x; x++) {
          this.listMatrix.push({
            id: y + 'y' + x + 'x',
            size: widthMatrix / this.value_x,
            x: x * widthMatrix / this.value_x,
            y: y * widthMatrix / this.value_x,
            color: this.index === x + y * this.value_x ? 'green' : 'white',
            value: ' ',
            // value_id: y + 'rectangle'
          });
        }
      }
    },
    keyEvent(e) {
      if (e.target.className === 'table-cell-content fill-width' || e.target.className === 'table-cell-content') {
        return
      }
      if (e.keyCode >= 37 && e.keyCode <= 40) {
        switch (e.keyCode) {
          case 37: // key left
            if (this.index !== 0) {
              if (this.selected === '2d') {
                if (this.index < this.listMatrix.length) {
                  this.startPositionMatrixChanged({target: {index: this.index - 1}})
                } else {
                  this.startPositionMatrixChanged({target: {index: 0}})
                }
              } else {
                this.startPositionRibbonChanged({target: {index: this.index - 1}})
              }
            }
            break
          case 38: // key up
            if (this.index - this.value_x >= 0 && this.selected === '2d') {
              if (this.index < this.listMatrix.length) {
                this.startPositionMatrixChanged({target: {index: this.index - this.value_x}})
              } else {
                this.startPositionMatrixChanged({target: {index: 0}})
              }
            }
            break
          case 39: // key right
            if (this.selected === 'ribbon') {
              if (this.index < this.ribbonText.length - 1) {
                this.startPositionRibbonChanged({target: {index: this.index + 1}})
              }
            } else {
              if (this.index < this.listMatrix.length - 1) {
                if (this.index < this.listMatrix.length) {
                  this.startPositionMatrixChanged({target: {index: this.index + 1}})
                } else {
                  this.startPositionMatrixChanged({target: {index: 0}})
                }
              }
            }
            break
          case 40: // key down
            if (this.index + this.value_x < this.listMatrix.length && this.selected === '2d') {
              if (this.index < this.listMatrix.length) {
                this.startPositionMatrixChanged({target: {index: this.index + this.value_x}})
              } else {
                this.startPositionMatrixChanged({target: {index: 0}})
              }
            }
            break
        }
      } else {
        if (this.selected === '2d') {
          if (48 <= e.keyCode && e.keyCode <= 90 || e.keyCode === 32) {
            this.listMatrix[this.index].value = e.key
            if (this.listMatrix.length - 1 !== this.index) {
              this.listMatrix[this.index].color = 'white'
              this.index += 1
              this.listMatrix[this.index].color = 'green'
            }

          } else if (e.keyCode === 8 && this.index !== 0) {
            this.listMatrix[this.index].value = ' '
            this.listMatrix[this.index].color = 'white'
            this.index -= 1
            this.listMatrix[this.index].color = 'green'
          }
        } else {
          //ribbon changing
          if (48 <= e.keyCode && e.keyCode <= 90 || e.keyCode === 32) {

            this.ribbonText = this.ribbonText.slice(0, this.index + 1) + e.key + this.ribbonText.slice(this.index + 1)
            this.index += 1

            this.createRibbon()
          }

          if (e.keyCode === 8 && this.ribbonText.length !== 1) {
            console.log(this.index, this.ribbonText.length)
            if (this.ribbonText.length - 1 === this.index) {

              this.ribbonText = this.ribbonText.slice(0, this.index)
              this.index -= 1

            } else {
              this.ribbonText = this.ribbonText.slice(0, this.index) + this.ribbonText.slice(this.index + 1)
              this.index -= 1
            }

            this.createRibbon()

          }
        }
      }

    },
    matrixChanged() {
      bus.$emit('matrixChanged', {
        "fieldSize": this.value_x,
        "startPosition": [0, 0]
      })
      this.createRectangles();
    },
    changeDimension() {
      bus.$emit('changeDimension', this.selected)
      this.selected !== '2d' ? this.createRibbon() : this.createRectangles();
      this.index = 0
    },
    ribbonChanged() {
      bus.$emit('ribbonChanged', this.ribbonText)
      this.value_x = this.ribbonText.length
      this.createRibbon()
    },
    createRibbon() {
      this.listRibbon = []
      for (let x = 0; x < this.ribbonText.length; x++) {
        this.listRibbon.push({
          id: x,
          size: 50,
          x: x * (50),
          y: 25,
          offset_x: 15,
          offset_y: 10,
          value: this.ribbonText[x],
          value_id: x + '/' + this.ribbonText[x],
          color: x === this.index ? 'green' : 'white'
        });
      }
      this.configKonvaRibbon.width = 50 * this.listRibbon.length
      bus.$emit('ribbonChanged', this.ribbonText)
    },
    startPositionMatrixChanged(e) {
      if (this.index < this.listMatrix.length) {
        this.listMatrix[this.index].color = 'white'
      }
      this.index = e.target.index;

      this.listMatrix[this.index].color = 'green';

      let y = Math.floor(this.index / this.value_x);
      let x = Math.floor(this.index % this.value_x);

      bus.$emit('startPosition', {point: [x, y]})
    },
    startPositionRibbonChanged(e) {
      if (this.index < this.listRibbon.length) {
        this.listRibbon[this.index].color = 'white';
        this.index = e.target.index
        this.listRibbon[this.index].color = 'green';

        bus.$emit('startPosition', {point: [this.index]})
      } else {
        this.index = 0;
        bus.$emit('startPosition', {point: [this.index]})
      }
    },
    redraw() {
      if (this.matrix !== [] && this.selected === '2d') {
        this.value_x = this.matrix.length;
        this.createRectangles()
        for (let y = 0; y < this.matrix.length; y++) {
          for (let x = 0; x < this.matrix.length; x++) {
            this.listMatrix[y * this.matrix.length + x].value = this.matrix[y][x];
          }
        }
      }
      if (this.selected === 'ribbon') {
        this.createRibbon();
      }
    }
  }
}
</script>

<style scoped>
.local {
  border: 2px solid #000000;
  background: lightgreen;
  min-width: 60%;
  min-height: 65vh;
  overflow: hidden;
  /*overflow-x: auto;*/
}

#canvasMatrix {
  height: 60vh;
  width: 60vh;
  /*border: 2px solid black;*/
  margin-left: auto;
  margin-right: auto;
  overflow: hidden
}

#canvasRibbon {
  height: 32.5vh;
  width: 100%;
  margin-top: 25%;
  /*margin-left: 45%;*/
  /*margin-right: 55%;*/
  overflow: hidden;
  overflow-x: auto;
}
</style>

<template>
  <div class="local">
    <b-row>
      <b-col>
        <b-form-select
            @change="changeDimension"
            v-model="selected"
            :options="options"></b-form-select>
      </b-col>

      <b-col>
        <b-form-input
            @change="ribbonChanged"
            v-if="selected==='ribbon'"
            v-model="ribbonText"
        ></b-form-input>

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

      <b-col v-if="selected==='2d'">
        <b-form-input
            @change="matrixChanged"
            v-model="startPosition"
        ></b-form-input>
      </b-col>

      <b-col>
        <b-button-group>
          <b-button @click="scalePlus">+</b-button>
          <b-button @click="scaleMinus">-</b-button>
        </b-button-group>
      </b-col>

    </b-row>
    <!--    <canvas id="canvasScene" class="field" style="border:1px solid #BBB;" v-insert-message=""></canvas>-->
  </div>
</template>

<script>
import {bus} from "@/main"

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
      value_x: 2,
      startPosition: "0, 0",
      ribbonText: "abababa"
    }
  },
  mounted() {
    bus.$on('draw scene', data => {
      this.matrix = data
      // console.log(data)
      this.redraw()
    })
  },
  methods: {
    matrixChanged() {
      bus.$emit('matrixChanged', {
        "fieldSize": this.value_x,
        "startPosition": this.startPosition
      })
    },
    changeDimension() {
      bus.$emit('changeDimension', this.selected)
    },
    ribbonChanged() {
      bus.$emit('ribbonChanged', this.ribbonText)
    },
    clearScene() {
      this.field = document.getElementById("canvasScene").getContext('2d');
      let width = this.field.scrollWidth;
      let height = this.field.scrollHeight;
      this.field.fillStyle = 'rgb(255, 255, 255)'
      this.field.fillRect(0, 0, width, height)
    },
    scalePlus() {
      // document.getElementById("canvasScene").getContext('2d').scale(1.04, 1.04)
      this.redraw()
    },
    scaleMinus() {
      // document.getElementById("canvasScene").getContext('2d').scale(0.96, 0.96)
      this.redraw()
    },
    redraw() {
      this.clearScene()
      if (this.matrix !== []) {
        // will be redone with
        // this.clearScene()
        // this.field = document.getElementById("canvasScene");
        // let width = this.field.width;
        // let height = this.field.height;
        // // let ceilWidth = width / this.matrix[0].length;
        // // let ceilHeight = width / this.matrix.length;
        // // console.log(height, width, ceilHeight, ceilWidth)
        // this.field = this.field.getContext('2d');
        //
        // this.field.fillStyle = 'rgb(255, 255, 255)'
        // for (let y = 0; y < this.matrix.length; y++) {
        //   for (let x = 0; x < this.matrix[0].length; x++) {
        //     this.field.fillRect(x * width / this.matrix[0].length, y * height / this.matrix.length,
        //         width / this.matrix[0].length, height / this.matrix.length)
        //   }
        // }
        //
        //
        // for (let y = 0; y < this.matrix.length; y++) {
        //   for (let x = 0; x < this.matrix[0].length; x++) {
        //     if (this.matrix[y][x] === "1") {
        //       this.field.fillStyle = 'rgb(255, 0, 0)'
        //       this.field.fillRect(x * width / this.matrix[0].length, y * height / this.matrix.length,
        //           width / this.matrix[0].length, height / this.matrix.length)
        //     }
        //   }
        // }
        //
        // this.field.fillStyle = 'rgb(0, 0, 0)'
        // for (let y = 1; y <= this.matrix.length; y++) {
        //   for (let x = 1; x <= this.matrix[0].length; x++) {
        //     this.field.beginPath();
        //     this.field.moveTo(width / this.matrix[0].length * x, 0);
        //     this.field.lineTo(width / this.matrix[0].length * x, height);
        //     this.field.stroke();
        //   }
        //   this.field.beginPath();
        //   this.field.moveTo(0, height / this.matrix.length * y);
        //   this.field.lineTo(width, height / this.matrix.length * y);
        //   this.field.stroke();
        // }
      }
    }
  }
}
</script>

<style scoped>
.local {
  border: 2px solid #000000;
  min-width: 60%;
  min-height: 65vh;
}

/*.field {*/
/*  min-width: 100vh;*/
/*  min-height: 65vh;*/
/*  overflow: auto;*/
/*}*/
</style>
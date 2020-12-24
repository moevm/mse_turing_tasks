<template>
  <div class="state-window">
    <b-container>
      <b-row>
        <div
            style="width: 30px; height: 30px"
        ></div>
        <div class=" hor-bttn"
             ref="vtcBttn"
             v-for="vButton in buttonsHorizontal"
             :key="vButton.id">
          <b-button
              variant="success"
              style="width: 90px; "
              v-on:click="removeColumn(vButton)"
          >-
          </b-button>
        </div>
      </b-row>
      <b-row>
        <div class="table-vertical">
          <b-button-group vertical>
            <div class=" "
                 v-for="hButton in buttonsVertical"
                 :key="hButton.id">
              <b-button
                  variant="success"
                  v-on:click="removeRow(hButton)"
                  style="height: 40px;width: 30px"
              >-
              </b-button>
            </div>
          </b-button-group>
          <div id="dynamic-table">
            <vue-table-dynamic
                :params="params"
                @cell-change="onCellChange"
            ></vue-table-dynamic>
          </div>
          <b-button @click="addColumn" type="submit" class="btn-sm">+</b-button>
        </div>
      </b-row>


      <b-button @click="addRow" type="submit" class="btn-sm">+</b-button>
    </b-container>
  </div>
</template>

<script>
import {bus} from "@/main"

export default {
  name: "StateWindow",
  data() {
    return {
      params: {
        data: [
          ['state/symbol', 'a', 'b', '\\s'],
          ['q0', 'r, b, q0', 'r, a, q1', 'r, \\s, q0'],
          ['q1', 'r, a, q1', 'r, a, q1', 'r, \\s, q1']
        ],
        border: true,
        edit: {
          row: [0, 1, 2]
        },
        columnWidth: [{column: 0, width: 90}, {column: 1, width: 90}, {column: 2, width: 90}, {column: 3, width: 90}],
        rowHeight: 40,
        scrollbar: 'hidden'
      },
      buttonsHorizontal: [0, 1, 2, 3],
      buttonsVertical: [0, 1, 2],

    }
  },
  created() {
  },
  mounted() {
    bus.$on('loadTable', () => {
      bus.$emit('tableChanged', this.params.data)
    })

    bus.$on("setTable", data => {
      this.params.data = []
      this.params.data.push([])
      let alphabet = [];
      for (let i in data.table) {
        for (let symbol in data.table[i]) {
          if (symbol === ' ') {
            alphabet.push('\\s')
          } else {
            alphabet.push(symbol)
          }
        }
        break
      }
      this.params.data[0][0] = 'state/symbol'
      for (let i = 0; i < alphabet.length; i++) {
        this.params.data[0][i + 1] = alphabet[i]
      }
      for (let i in data.table) {
        this.params.data.push([])
        this.params.data[this.params.data.length - 1].push(i)
        for (let symbol in data.table[i]) {
          let cell = data.table[i][symbol]
          this.params.data[this.params.data.length - 1].push(`${cell.move}, ${cell.write === ' ' ? '\\s' : cell.write}, ${cell.state}`)
        }
      }
      this.params.edit.row = []
      this.buttonsHorizontal = []
      this.buttonsVertical = []
      for (let i = 0; i < this.params.data[0].length; i++) {
        this.params.columnWidth.push({column: i, width: 90})
        this.buttonsHorizontal.push(i)
      }
      for (let i = 0; i < this.params.data.length; i++) {
        this.params.edit.row.push(i)
        this.buttonsVertical.push(i)
      }
    })
  },
  methods: {
    onCellChange(rowIndex, columnIndex, data) {
      this.params.data[rowIndex][columnIndex] = data
      bus.$emit('tableChanged', this.params.data)
    },
    addRow() {
      if (this.params.data.length < 18) {
        this.params.data.push([...Array(this.params.data[0].length)]);
        this.params.edit.row.push(this.params.edit.row.length);
        this.buttonsVertical.push(this.buttonsVertical.length)
      }
    },
    removeRow(rowIndex) {
      if (this.params.data.length > 2) {
        this.params.data.splice(rowIndex, 1)
        this.params.edit.row.pop()
        this.buttonsVertical.pop()
      }
    },
    addColumn() {
      if (this.params.data[0].length <= 21) {
        for (let i = 0; i < this.params.data.length; i++) {
          this.params.data[i].push("")
        }
        this.buttonsHorizontal.push(this.buttonsHorizontal.length)
        this.params.columnWidth.push({
          column: this.buttonsVertical.length - 1,
          width: 90
        })
      }
    },
    removeColumn(columnIndex) {
      if (this.params.data[0].length > 2) {
        for (let i = 0; i < this.params.data.length; i++) {
          this.params.data[i].splice(columnIndex, 1)
        }
        this.buttonsHorizontal.pop()
        this.params.columnWidth.pop()
      }
    },

  }

}
</script>

<style scoped>
.state-window {
  border: 2px solid #000;
  min-width: 40%;
  min-height: 100%;
  overflow: auto;
}

.table-vertical {
  display: flex;
}

.hor-bttn {
  /*border: black 1px solid;*/
}

#dynamic-table {
  width: 100%;
  min-height: 100%;
}
</style>

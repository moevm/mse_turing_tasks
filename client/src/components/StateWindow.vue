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
  columnWidth: 100,
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
    this.resizeButtons()
  },
  mounted() {
    bus.$on('loadTable', () => {
      bus.$emit('tableChanged', this.params.data)
    })
    this.resizeButtons()
  },
  methods: {
    resizeButtons() {
      // this.buttonSizeHorizontal.width = `${document.getElementById('dynamic-table').clientWidth / this.buttonsHorizontal.length}px`
      // this.buttonSizeHorizontal.height = `${document.getElementById('dynamic-table').clientHeight / this.buttonsVertical.length}px`
    },
    onCellChange(rowIndex, columnIndex, data) {
      this.params.data[rowIndex][columnIndex] = data
      bus.$emit('tableChanged', this.params.data)
    },
    addRow() {
      if (this.params.data.length < 18) {
        this.params.data.push([...Array(this.params.data[0].length)]);
        this.params.edit.row.push(this.params.edit.row.length);
        this.buttonsVertical.push(this.buttonsVertical.length)
        this.resizeButtons()
      }
    },
    removeRow(rowIndex) {
      if (this.params.data.length > 2) {
        this.params.data.splice(rowIndex, 1)
        this.params.edit.row.pop()
        this.buttonsVertical.pop()
        this.resizeButtons()
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
        this.resizeButtons()
      }
    },
    removeColumn(columnIndex) {
      if (this.params.data[0].length > 2) {
        for (let i = 0; i < this.params.data.length; i++) {
          this.params.data[i].splice(columnIndex, 1)
        }
        this.buttonsHorizontal.pop()
        this.params.columnWidth.pop()
        this.resizeButtons()
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

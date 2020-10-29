<template>
  <div class="state-window">
    <b-container>
      <!--   finish the styles   -->
      <b-button variant="invisible"></b-button>
      <!--      -->
      <div class="btn-group-vertical align-items-center"
           v-for="vButton in buttonsHorizontal"
           :key="vButton.id">
        <b-button
            variant="danger"
            v-on:click="removeColumn(vButton)"
        >-
        </b-button>
      </div>
      <div class="table-vertical">
        <b-button-group vertical>
          <div class="align-items-center btn-group-vertical"
               v-for="hButton in buttonsVertical"
               :key="hButton.id">
            <b-button
                variant="primary"
                v-on:click="removeRow(hButton)"
                class="btn-sm"
            >-
            </b-button>
          </div>
        </b-button-group>

        <vue-table-dynamic
            :params="params"
            @cell-change="onCellChange"
        ></vue-table-dynamic>
        <b-button @click="addColumn" type="submit" class="btn-sm">+</b-button>

      </div>
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
          ['state/symbol', 'a', 'b'],
          ['q0', 'l, b, q0', 'l, a, q1'],
          ['q1', 'l, a, q1', 'l, a, q1']
        ],
        border: true,
        edit: {
          row: [0, 1, 2]
        },
        scrollbar: 'hidden'
      },
      buttonsHorizontal: [0, 1, 2],
      buttonsVertical: [0, 1, 2]
    }
  },
  mounted() {
    bus.$on('loadTable', () => {
      bus.$emit('tableChanged', this.params.data)
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
      // console.log(parseInt(rowIndex), "row")
      if (this.params.data.length > 2) {
        // console.log('before', this.params.data)
        this.params.data.splice(rowIndex, 1)
        // console.log('after', this.params.data)
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
      }
    },
    removeColumn(columnIndex) {
      if (this.params.data[0].length > 2) {
        for (let i = 0; i < this.params.data.length; i++) {
          this.params.data[i].splice(columnIndex, 1)
        }
        this.buttonsHorizontal.pop()
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
</style>
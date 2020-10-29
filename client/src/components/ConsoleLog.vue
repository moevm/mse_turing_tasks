<template>
  <div class="console">
    <li v-for="item in consoleString" :key="item.id">
      {{ item }}
    </li>
  </div>
</template>

<script>
import {bus} from '@/main';

export default {
  name: "ConsoleLog",
  data() {
    return {
      consoleString: []
    }
  },
  mounted() {
    bus.$on('clicked', data => {
      this.consoleString.push(data)
    })

    bus.$on('getAnswer', data => {
      this.consoleString.push(data)
    })
  }
}
</script>

<style scoped>
.console {
  width: 100%;
  height: 35vh;
  border: 2px solid #000000;
  background: darkgrey;
  overflow: auto;
}
</style>
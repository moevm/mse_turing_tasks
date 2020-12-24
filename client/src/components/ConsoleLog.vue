<template>
  <div class="console" id="container" ref="container">
    <li v-for="item in consoleString" :key="item.id" class="text-black">
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
      var container = this.$refs.container;
      container.scrollTop = container.scrollHeight + 120;
    })

    bus.$on('getAnswer', data => {
      this.consoleString.push(data)
      var container = this.$refs.container;
      container.scrollTop = container.scrollHeight + 120;
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

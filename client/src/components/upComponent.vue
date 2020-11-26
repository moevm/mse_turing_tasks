<template>
  <div class="upComp">
    <StateWindow class="state-window"></StateWindow>
    <EndlessRibbon></EndlessRibbon>
  </div>
</template>

<script>
import StateWindow from "@/components/StateWindow";
import EndlessRibbon from "@/components/EndlessRibbon";

export default {
  name: "upComponent",
  components: {StateWindow, EndlessRibbon}

}

</script>

<style scoped>
.upComp {
  display: flex;
  min-height: 65vh;
  /*width: 100vh;*/
}
.state-window {
  overflow: auto;
}
</style>

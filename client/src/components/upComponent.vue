<template>
  <div class="upComp">
    <StateWindow></StateWindow>
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
  width: 100%;
  height: 600px;
}
</style>
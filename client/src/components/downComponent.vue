<template>
  <div class="downComp">
    <buttonsArea></buttonsArea>
    <ConsoleLog></ConsoleLog>
  </div>
</template>

<script>
import buttonsArea from "@/components/buttonsArea";
import ConsoleLog from "@/components/ConsoleLog";

export default {
  name: "downComponent",
  components: { buttonsArea, ConsoleLog}

}
</script>

<style scoped>
.downComp {
  display: flex;
  width: 100%;
  height: 250px;
}
</style>
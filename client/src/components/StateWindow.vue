<template>
<div class="state-window">
  <div class="plug">
    Таблица состояний
  </div>
</div>
</template>

<script>
export default {
name: "StateWindow"
}
</script>

<style scoped>
.state-window {
  border: 2px solid #000;
  width: 60%;
}
.plug {
  text-align: center;
  height: 50%;
  transform: translate(0, 50%)
}
</style>
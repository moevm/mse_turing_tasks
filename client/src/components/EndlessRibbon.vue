<template>
<div class="local">
  <div class="plug">
    Лента/Плоскость
  </div>
</div>
</template>

<script>
export default {
name: "EndlessRibbon"
}
</script>

<style scoped>
.local {
  border: 2px solid #000000;
  min-width: 50%;
  min-height: 50%;
  margin: 0px auto;
}
.plug {
  text-align: center;
  height: 50%;
  transform: translate(0, 50%)
}
</style>
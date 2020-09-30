<template>
  <div class="buttons">
    <p>
      <button class="change">Change dimension</button>
      <button class="start">Start/Continue</button>
    </p>
    <p>
      <button class="openFIle">Open file</button>
      <button class="Stop">Stop</button>
    </p>
    <p>
      <button class="save">Save file</button>
      <button class="step">Step</button>
    </p>

  </div>
</template>

<script>
export default {
  name: "buttonsArea"
}
</script>

<style scoped>
.buttons {
  border: 2px solid #000000;
  width: 30%;
  height: 100%;
}

.change, .save, .start, .openFIle, .Stop, .save, .step {
  width: 30%;
  height: 25px;

}
</style>
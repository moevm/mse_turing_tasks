<template>
  <div class="page">
    <div class="upComponent">
      <upComponent></upComponent>
    </div>
    <div class="downComponent">
      <downComponent></downComponent>
    </div>

  </div>
</template>

<script>
import upComponent from "@/components/upComponent";
import downComponent from "@/components/downComponent";


export default {
  name: 'app',
  data() {
    return {}
  },
  components: {
    upComponent, downComponent
  },
  methods: {}
}
</script>

<style>
.page {
  background: #FFEFD5;
  min-height: 100vh;
  overflow:hidden;
}
.upComponent {
  min-height: 65vh;
  min-width: 100vh;
}
.downComponent {
  min-height: 35vh;
}
</style>
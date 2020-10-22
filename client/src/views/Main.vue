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
  width: 100%;
  height: 100%;
}
.upComponent {
  height: 65%;
}
.downComponent {
  height: 35%;
}
</style>
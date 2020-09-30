<template>
  <div class="page">
    <upComponent></upComponent>
    <downComponent></downComponent>
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
</style>
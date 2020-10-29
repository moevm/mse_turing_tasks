import Vue from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import VueTableDynamic from 'vue-table-dynamic'
import BootstrapVue from 'bootstrap-vue';
import router from "./router";

export const bus = new Vue();

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(VueTableDynamic)

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
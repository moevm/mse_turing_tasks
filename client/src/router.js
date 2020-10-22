import Vue from 'vue'
import Router from 'vue-router'
import Authorization from "@/views/Authorization";
Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            component: Authorization
        },
        {
            path: '/main',
            // path: '/',
            component: () => import('./views/Main.vue')
        }
    ]
})
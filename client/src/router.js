import Vue from 'vue'
import Router from 'vue-router'
import Authorization from "@/views/Authorization";

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'Authorization',
            component: Authorization
        },
        {
            path: '/main',
            name: 'Turing machine',
            component: () => import('./views/Main.vue')
        }
    ]
})
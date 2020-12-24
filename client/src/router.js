import Vue from 'vue'
import Router from 'vue-router'
import Authorization from "@/views/Authorization";
import Main from "@/views/Main";

Vue.use(Router)

let router = new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'Authorization',
            meta: {
                requiresAuth: false
            },
            component: Authorization
        },
        {
            path: '/main',
            name: 'TuringMachine',
            meta: {
                requiresAuth: true
            },
            component: Main
        }
    ]
})

export default router;

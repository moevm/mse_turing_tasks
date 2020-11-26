import Vue from 'vue'
import Router from 'vue-router'
import Authorization from "@/views/Authorization";
import Main from "@/views/Main";

Vue.use(Router)

// раскомментировать, когда дима напишет авторизацию

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

// router.beforeEach((to, from, next) => {
//     console.log(to, from, next);
//     if (to.path === '/main' && to.matched.some(record => record.meta.requiresAuth)) {
//         if (localStorage.getItem('token') === null) {
//             router.push('/')
//         } else {
//             router.push('/main')
//         }
//     } else {
//         next()
//     }
// })

// router.beforeEach((to, from, next) => {
//     if (to.matched.some(record => record.meta.requiresAuth)) {
//         if (localStorage.getItem('token') === null) {
//             next({
//                 name: 'Authorization',
//                 query: {redirect: to.fullPath}
//             })
//         } else {
//             next({
//                 name: 'TuringMachine',
//                 query: {redirect: to.fullPath}
//             })
//
//         }
//     }  else {
//         next()
//     }
// })

export default router;

// Example of how to use Vue Router

import { Router, createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import UsersPage from '../pages/UsersPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';

let base: string = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router: Router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/users/', name: 'Users Page', component: UsersPage },
        { path: '/profile/', name: 'Profile Page', component: ProfilePage },
    ]
})

export default router

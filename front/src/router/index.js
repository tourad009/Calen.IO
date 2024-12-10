import { createRouter, createWebHistory } from 'vue-router';

const routes = [
    {
        path: '/', // Route racine
        redirect: '/login' // Redirige vers la page login par défaut
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/login.vue')
    },
    {
        path: '/calendar',
        name: 'DemoApp',
        component: () => import('../views/calendar.vue')
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;

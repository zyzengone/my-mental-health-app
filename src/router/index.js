import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import MentalHealthAssessment from '../views/MentalHealthChat.vue';
import ChatPage from '../views/ChatPage.vue';
import KnowledgeGraph from '../views/KnowledgeGraph.vue';
import Login from "../views/Login.vue";
import { ElMessage } from 'element-plus'

const routes = [
    {
        path: '/',
        name: 'chat',
        component: ChatPage,
        meta: { requiresAuth: true }
    },
    {
        path: '/mental-health-assessment',
        name: 'MentalHealthAssessment',
        component: MentalHealthAssessment,
        meta: { requiresAuth: true }
    },
    {
        path: '/chat',
        name: 'ChatPage',
        component: ChatPage,
        meta: { requiresAuth: true }
    },
    {
        path: '/knowledge-graph',
        name: 'KnowledgeGraph',
        component: KnowledgeGraph,
        meta: { requiresAuth: true }
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/profile',
        name: 'Profile',
        component: () => import('../views/Profile.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/admin',
        name: 'Admin',
        component: () => import('../views/Admin.vue'),
        // meta: { requiresAuth: true, requiresAdmin: true }
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
    const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin)
    const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true'
    const isAdmin = localStorage.getItem('isAdmin') === 'true'
    
    if (requiresAuth && !isAuthenticated) {
        next({ name: 'Login' })
    } else if (requiresAdmin && !isAdmin) {
        ElMessage.error('无管理员权限')
        next(from.path)
    } else {
        next()
    }
})

export default router;

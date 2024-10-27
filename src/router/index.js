import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import MentalHealthAssessment from '../views/MentalHealthChat.vue';
import ChatPage from '../views/ChatPage.vue';
import KnowledgeGraph from '../views/KnowledgeGraph.vue';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
    },
    {
        path: '/mental-health-assessment',
        name: 'MentalHealthAssessment',
        component: MentalHealthAssessment,
    },
    {
        path: '/chat',
        name: 'ChatPage',
        component: ChatPage,
    },
    {
        path: '/knowledge-graph',
        name: 'KnowledgeGraph',
        component: KnowledgeGraph,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;

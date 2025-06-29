import { createApp } from 'vue';
import App from './App.vue';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import router from './router';
import pinia from './store';

const app = createApp(App);
app.config.globalProperties.$apiUrl = 'http://localhost:8080';
app.use(ElementPlus);
app.use(router);
app.use(pinia)
app.mount('#app');

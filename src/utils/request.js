//引入axios请求
import axios from 'axios'
//引入element-plus里面的消息提示
import { ElMessage } from 'element-plus'
import {useRouter} from "vue-router";
import {useUserStore} from "../store/index.js";

const BASE_API='http://localhost:8080'
// const BASE_API="http://mental.lmlzy.link:7397"
// 创建axios实例
const service = axios.create({
    baseURL: BASE_API, //所有的后端接口请求地址前缀部分(没有后端请求不用写)
    timeout: 40000, // 请求超时时间,这里15秒
    //withCredentials: true,// 异步请求携带cookie,true为携带,false为不携带
    //请求头里面设置通用传参类型
    // headers: {
    //   //设置后端需要的传参类型
    //   'Content-Type': 'application/json',
    // }
})

// request拦截器
// request拦截器
service.interceptors.request.use(config => {
    // 检查请求路径是否为登录请求
    if (!config.url.includes('/login')) {
        const token = localStorage.getItem('token');
        config.headers['Authorization'] = `${token}`; // 让每个请求携带自定义token 请根据实际情况自行修改
    }
    return config
}, error => {
    console.log(error)
    Promise.reject(error)
})


// response拦截器
service.interceptors.response.use(
    response => {
        //对数据返回做什么
        return response.data
    },
    error => {
        console.log('err' + error)
        if (error.response && error.response.status === 403) {
            console.log(error)
            // 清除本地存储中的 token 和认证状态
            localStorage.removeItem('token');
            localStorage.removeItem('isAuthenticated');

            // 在组件中处理重定向
            throw new Error('Unauthorized');
        } else {
            ElMessage({
                message: error.message,
                type: 'error',
                duration: 3 * 1000
            })
        }
        return Promise.reject(error)
    }
)

export default service

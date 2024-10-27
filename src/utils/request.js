//引入axios请求
import axios from 'axios'
//引入element-plus里面的消息提示
import { ElMessage } from 'element-plus'

// const BASE_API="http://localhost:8080"
const BASE_API="http://mental.lmlzy.link:7397"
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
service.interceptors.request.use(config => {
    /*if (store.getters.token) {
      config.headers['Authorization'] = getToken() // 让每个请求携带自定义token 请根据实际情况自行修改
    }*/
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
        ElMessage({
            message: error.message,
            type: 'error',
            duration: 3 * 1000
        })
        return Promise.reject(error)
    }
)

export default service
